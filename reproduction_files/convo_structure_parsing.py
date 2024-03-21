"""Parses a structured conversation dataset (a Corpus) from Cornell's ConvoKit
library into a NetworkX network object.
"""

import networkx as nx
from convokit import Conversation, Corpus


def check_conversation_integrity(convo: Conversation) -> bool:
    """Check conversation integrity for a complete reply-to chain
    (from conversation.id root to leaves)
    """
    if convo.check_integrity():
        return True
    print(f"Conversation {convo.id} is not intact.")
    return False


def change_deleted_speaker_id(speaker_id: str, deleted_speaker_id: int) -> str:
    """Change a speaker ID to a unique string if it is [deleted]. When Reddit
    users delete their account, post, or comment, their username or comment is
    replaced with [deleted]."""
    if speaker_id == "[deleted]":
        return f"deleted_speaker_{deleted_speaker_id}"
    return speaker_id


def get_subreddit_speakers(corpus: Corpus) -> tuple[dict, dict]:
    """Returns 1) speakers who participated in a subreddit by commenting and
    2) a speaker's list of subreddits.

    Note: speaker names with 'bot' and '[deleted]' should be handled before this
    data alone can be informative.
    """
    # A subreddit's speakers
    subreddit_users = {}

    for conv in corpus.iter_conversations():
        # get speakers in conversation
        speakers = conv.get_speaker_ids()
        subreddit = conv.retrieve_meta('subreddit')
        if subreddit not in subreddit_users:
            subreddit_users[subreddit] = set()
        subreddit_users[subreddit].update(speakers)

    # A speaker's subreddits
    user_subbredits = {}
    for sub, speakers in subreddit_users.items():
        for id in speakers:
            user_subbredits.setdefault(id, []).append(sub)

    return (subreddit_users, user_subbredits)


def parse_reddit_convo_structure(corpus: Corpus) -> nx.MultiDiGraph:
    """Parse a structured Corpus dataset into a network."""

    convo_graph = nx.MultiDiGraph()
    deleted_speaker_id = 0
    # Node attribute later that needs updating as we fix deleted speakers
    subreddit_users, user_subbredits = get_subreddit_speakers(corpus)

    # starting from utterances and replies, construct edges,
    # which will initialize sepakers as nodes
    for convo in corpus.iter_conversations():
        sub = convo.retrieve_meta('subreddit')

        if not check_conversation_integrity(convo):
            continue

        convo_paths = []
        for path in convo.get_root_to_leaf_paths():
            convo_paths.append([utt.id for utt in path])

        for path in convo_paths:
            # magic number 2 skips the first utterance because it's the post itself
            for utt_id in path[2:]:
                from_speaker = change_deleted_speaker_id(
                    convo.get_utterance(utt_id).speaker.id,
                    deleted_speaker_id
                )
                to_speaker = change_deleted_speaker_id(
                    convo.get_utterance(path[path.index(utt_id)-1]).speaker.id,
                    deleted_speaker_id
                )
                # Add edges and edge attributes
                convo_graph.add_edge(
                    from_speaker,
                    to_speaker,
                    key=utt_id,
                    convo_id=convo.id,
                    utt_id=utt_id,
                    utt_text=convo.get_utterance(utt_id).text,
                    utt_speaker=convo.get_utterance(utt_id).speaker.id,
                    utt_timestamp=convo.get_utterance(utt_id).timestamp,
                    utt_score=convo.get_utterance(utt_id).meta['score']
                )
                # Add new user ID to user_subreddits
                if from_speaker not in user_subbredits:
                    user_subbredits[from_speaker] = [sub]

        deleted_speaker_id += 1

    # Add node attributes (this will not add "[deleted]" or isolated nodes--submitters who
    # have 0 comments reflected in this corpus)
    for s in corpus.iter_speakers():
        # check if s is not a node
        if s.id not in convo_graph.nodes:
            continue
        # set existing node attributes
        convo_graph.nodes[s.id]['num_comments'] = s.meta['num_comments']
        convo_graph.nodes[s.id]['num_posts'] = s.meta['num_posts']
        convo_graph.nodes[s.id]['subreddits'] = user_subbredits[s.id]

    return convo_graph


def two_convo_sample(corpus: Corpus) -> tuple[Corpus, nx.MultiDiGraph]:
    """Parse a specific sample of two conversations from a structured Reddit
    Corpus dataset into a new Corpus and a network.

    Note: this sample has 2 conversations sharing at least 1 user for the
    purposes of validation and tests.
    """

    conv = corpus.get_conversation('9fio59')
    conv2 = corpus.get_conversation('9gthts')

    # Combine conversations into a list of Utterance objects
    # (this small example loses the Conversation object type but retains all other types)
    test_list_utterances = list(conv.iter_utterances()) + list(conv2.iter_utterances())
    # Create a new Corpus object
    new_corpus = Corpus(utterances=test_list_utterances)

    G = parse_reddit_convo_structure(new_corpus)
    return (new_corpus, G)


def parse_reddit_convo_structure_digraph(corpus: Corpus) -> nx.DiGraph:
    """Parse a structured Corpus dataset into a weighted network.

    Note: edges represent accumulated weight, so we lose the ability to keep all
    utterance information.
    TODO: Some thought has to go into representing this info via proxy edge and
    node attributes.
    """
    convo_graph = nx.DiGraph()
    deleted_speaker_id = 0
    # Node attribute later that needs updating as we fix deleted speakers
    subreddit_users, user_subbredits = get_subreddit_speakers(corpus)

    # starting from utterances and replies, construct edges,
    # which will initialize sepakers as nodes
    for convo in corpus.iter_conversations():
        sub = convo.retrieve_meta('subreddit')
        from_speaker_weights = {x: 0 for x in convo.get_speaker_ids()}

        if not check_conversation_integrity(convo):
            continue

        convo_paths = []
        for path in convo.get_root_to_leaf_paths():
            convo_paths.append([utt.id for utt in path])

        for path in convo_paths:
            # magic number 2 skips the first utterance because it's the post itself
            for utt_id in path[2:]:
                from_speaker = change_deleted_speaker_id(
                    convo.get_utterance(utt_id).speaker.id,
                    deleted_speaker_id
                )
                to_speaker = change_deleted_speaker_id(
                    convo.get_utterance(path[path.index(utt_id)-1]).speaker.id,
                    deleted_speaker_id
                )
                # Add new user ID to user_subreddits and edge weight tracking
                if from_speaker not in user_subbredits:
                    user_subbredits[from_speaker] = [sub]
                    from_speaker_weights[from_speaker] = 0
                from_speaker_weights[from_speaker] += 1

                # Add edges and edge attributes
                convo_graph.add_edge(
                    from_speaker,
                    to_speaker,
                    weight=from_speaker_weights[from_speaker]
                )

        deleted_speaker_id += 1

    # Add node attributes (this will not add "[deleted]" or isolated nodes--submitters who
    # have 0 comments reflected in this corpus)
    for s in corpus.iter_speakers():
        # check if s is not a node
        if s.id not in convo_graph.nodes:
            continue
        # set existing node attributes
        convo_graph.nodes[s.id]['num_comments'] = s.meta['num_comments']
        convo_graph.nodes[s.id]['num_posts'] = s.meta['num_posts']
        convo_graph.nodes[s.id]['subreddits'] = user_subbredits[s.id]

    return convo_graph

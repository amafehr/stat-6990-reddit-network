# Small Reddit Corpus as a Network

This project explored how a corpus from a discussion forum might be explored as a network. I chose a small Reddit corpus for this purpose. The small Reddit corpus presents a sampling of 100 highly active subreddits from 2018 gathered from Pushshift.io and has open source through ConvoKit (at a minimum).

As a social network, Reddit presents a discussion forum-based structure with membership to many communities. It is a structure other social networks use, so the purpose here was to explore how turning a post into multiple conversations opens up research questions into community and well-being.

The structure of this network follows:
- Each top-level comment in a post is a conversation thread without a link back to a topic node.
- Latent meaning: engaged user participation; note that the conceptualization of information propagation or diffusion is somewhat different here than one might expect of a social network.
- Nodes: users
- Edges: reply-to

## Structure

- The python notebook presents some code and exploration while `convo_structure_parsing.py` is functionality to reproduce the network file.
- `reddit_small_corpus_network.gml.gz` is a compressed `.gml` network file.
- `reddit_small_corpus_network_card.json` is a concise summary of the network.

## Licenses and disclaimers

The license applicable to the network data is ODC-BY (see `DATA_LICENSE.txt`). Otherwise the MIT license applies to code in this repository (see `LICENSE.txt`).

The content of posts has not been filtered for profanity or offensive references.

## Resources

[ConvoKit](https://github.com/CornellNLP/ConvoKit/blob/master/examples/Introduction_to_ConvoKit.ipynb)
[Reddit Corpus (small)](https://convokit.cornell.edu/documentation/reddit-small.html)

## Notes:
- This is a work in progress.
- The current implementation is specific to Reddit datasets loaded using ConvoKit.
- Some shorthand variable names refer to object types: "convo" for Conversation, "utt" for Utterance.

I am making the following assumptions:
- Each top level comment within a post is represented as a conversation, with
the top level comment removed.
- Nodes are users and edges are replies (out-going is a reply from one user
(source) to another user (target)).
- AutoModerator and Auto- may make posts but do not appear to be a concern for having initiated top-level comments.
- deleted users and comments are represented as `[deleted]` in the dataset;
deleted comments remain but deleted users are recoded to one unique ID "deleted_#" per Conversation ID. This was deliberate to 1) preserve the conversation reply-to chain, and 2) to make the assumption that deleted users within a post could be some of the same person. This is a simplifying assumption under research. For instance, the more time distributed between earlier messages in the dataset's distribution of timestamps and 2018 (when this data was gathered), the more confounding variables and variance we cannot account for in terms of why we see [deleted] and what users that tag represents. This unknown area may affect the simplifying assumption of using one deleted_speaker_ID per post versus changing them all to be unique per top-level comment branch.


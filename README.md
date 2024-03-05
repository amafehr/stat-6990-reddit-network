# Small Reddit Corpus as a Network

This project explored how a corpus from a discussion forum might be explored as a network. I chose a small Reddit corpus for this purpose. The small Reddit corpus presents a sampling of 100 highly active subreddits from 2018 gathered from Pushshift.io and has open source through ConvoKit (at a minimum).

As a social network, Reddit presents a discussion forum-based structure with membership to many communities. It is a structure other social networks use, so the purpose here was to explore how turning a post into multiple conversations opens up research questions into community and well-being.

The structure of this network follows:
- Each top-level comment in a post is a conversation thread without a link back to a topic node.
- Latent meaning: ... TODO
- Nodes: users
- Edges: reply-to

## Structure

- The python notebook presents some code and exploration while `convo_structure_parsing.py` is functionality to reproduce the network file.
- `reddit_small_corpus_network.gml.gz` is a compressed `.gml` network file.
- `reddit_small_corpus_network_card.json` is a concise summary of the network.

## Licenses

The license applicable to the network data is ODC-BY (see `LICENSE.txt`). Otherwise the MIT license applies to code in this repository.

## Resources

[ConvoKit](https://github.com/CornellNLP/ConvoKit/blob/master/examples/Introduction_to_ConvoKit.ipynb)



## Notes:
- This is a work in progress.
- The current implementation is specific to the Reddit dataset.
- Some shorthand is used for variable names that refer to object types: "convo" for Conversation,
 "utt" for Utterance.
- I am making the following assumptions:
    - Each top level comment within a post is represented as a conversation, with
    the top level comment removed.
    - Nodes are users and edges are replies (out-going is a reply from one user
    (source) to another user (target)).
    - AutoModerator and Auto- may make posts but do not appear to be a concern for having initiated top-level comments.
    - deleted users and comments are represented as `[deleted]` in the dataset;
    deleted comments remain but deleted users are changed to one unique ID "deleted_#"
    per Conversation ID. This was deliberate to 1) preserve the conversation reply-to chain,
    and 2) to make the assumption that deleted users within a post could be some of the
    same person. This is a simplification and could be further researched.
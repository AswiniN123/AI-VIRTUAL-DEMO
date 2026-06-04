NLP_KNOWLEDGE = [
    {
        "topic": "NLP Pipeline",
        "aliases": ["nlp", "natural language processing", "text preprocessing"],
        "content": (
            "An NLP pipeline often includes text cleaning, tokenization, vectorization or embeddings, "
            "model processing, and finally a task output such as classification, translation, or generation."
        ),
        "category": "nlp"
    },
    {
        "topic": "Tokenization",
        "aliases": ["tokenization", "tokenizer", "tokens"],
        "content": (
            "Tokenization splits text into smaller units such as words, subwords, or characters. "
            "These tokens are then converted into numerical form for NLP models."
        ),
        "category": "nlp"
    },
    {
        "topic": "Embeddings",
        "aliases": ["embedding", "embeddings", "vector representation"],
        "content": (
            "Embeddings convert words, sentences, or items into dense numeric vectors. "
            "Similar meanings are often placed close together in embedding space."
        ),
        "category": "nlp"
    },
    {
        "topic": "Word2Vec and GloVe",
        "aliases": ["word2vec", "glove", "word embeddings"],
        "content": (
            "Word2Vec and GloVe are classic methods for learning vector representations of words so that similar words have similar vectors."
        ),
        "category": "nlp"
    },
    {
        "topic": "Transformer and Attention",
        "aliases": ["transformer", "transformers", "attention", "self attention", "multi head attention"],
        "content": (
            "Transformers use attention to let each token focus on other relevant tokens in the sequence. "
            "Self-attention captures context efficiently, which is why transformers work so well in NLP."
        ),
        "category": "nlp"
    },
    {
        "topic": "Attention Mechanism",
        "aliases": ["attention mechanism", "cross attention"],
        "content": (
            "Attention lets a model focus more on the most relevant parts of the input. "
            "Self-attention compares tokens within the same sequence, while cross-attention connects different sequences."
        ),
        "category": "nlp"
    },
    {
        "topic": "Positional Encoding",
        "aliases": ["positional encoding", "position embedding", "position embeddings"],
        "content": (
            "Transformers do not naturally understand order, so positional encoding gives each token information about its position in the sequence."
        ),
        "category": "nlp"
    },
    {
        "topic": "Seq2Seq",
        "aliases": ["seq2seq", "sequence to sequence", "encoder decoder"],
        "content": (
            "Sequence-to-sequence models map one sequence to another, such as translating one sentence into another language."
        ),
        "category": "nlp"
    },
    {
        "topic": "Named Entity Recognition",
        "aliases": ["ner", "named entity recognition"],
        "content": (
            "Named entity recognition identifies and labels entities in text such as people, locations, organizations, and dates."
        ),
        "category": "nlp"
    },
    {
        "topic": "Sentiment Analysis",
        "aliases": ["sentiment analysis", "sentiment classification"],
        "content": (
            "Sentiment analysis predicts whether text expresses positive, negative, or neutral opinion."
        ),
        "category": "nlp"
    },
    {
        "topic": "LLMs",
        "aliases": ["llm", "llms", "large language model", "large language models"],
        "content": (
            "Large language models are transformer-based systems trained on huge text datasets to predict the next token and perform many language tasks."
        ),
        "category": "nlp"
    },
    {
        "topic": "Prompt Engineering",
        "aliases": ["prompt engineering", "prompt", "system prompt", "few shot"],
        "content": (
            "Prompt engineering means designing instructions and examples so a language model produces more reliable outputs."
        ),
        "category": "nlp"
    },
    {
        "topic": "Bag of Words and TF-IDF",
        "aliases": ["bag of words", "bow", "tf idf", "tf-idf", "term frequency inverse document frequency"],
        "content": (
            "Bag of Words represents text by word counts, while TF-IDF gives higher weight to words that are important in a document but not common everywhere."
        ),
        "category": "nlp"
    },
    {
        "topic": "Stemming and Lemmatization",
        "aliases": ["stemming", "lemmatization", "stemmer", "lemmatizer"],
        "content": (
            "Stemming reduces words to crude roots, while lemmatization reduces them to meaningful dictionary forms."
        ),
        "category": "nlp"
    },
    {
        "topic": "BERT",
        "aliases": ["bert", "bidirectional encoder representations from transformers", "masked language model"],
        "content": (
            "BERT is a transformer encoder model trained with masked language modeling. "
            "It is strong for understanding tasks such as classification, question answering, and NER."
        ),
        "category": "nlp"
    },
    {
        "topic": "Decoder-only Language Models",
        "aliases": ["decoder only model", "decoder-only model", "gpt", "autoregressive model", "causal language model"],
        "content": (
            "Decoder-only models generate text token by token from left to right. "
            "They are widely used in chatbots, code generation, and open-ended text generation."
        ),
        "category": "nlp"
    },
    {
        "topic": "RAG",
        "aliases": ["rag", "retrieval augmented generation", "retrieval-augmented generation"],
        "content": (
            "RAG combines document retrieval with language generation so the model can answer using external knowledge instead of only its internal parameters."
        ),
        "category": "nlp"
    }
]

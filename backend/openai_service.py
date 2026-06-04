import json
import os
import re

from groq import Groq


GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY not found. Add it to your .env file.")

client = Groq(api_key=GROQ_API_KEY)


def normalize_topic(topic):
    lowered = (topic or "").lower()
    mapping = [
        ("transformer", "transformer"),
        ("attention", "transformer"),
        ("cnn", "cnn"),
        ("convolutional neural network", "cnn"),
        ("rnn", "rnn"),
        ("recurrent neural network", "rnn"),
        ("lstm", "rnn"),
        ("nlp pipeline", "nlp_pipeline"),
        ("natural language processing", "nlp_pipeline"),
        ("machine learning pipeline", "ml_pipeline"),
        ("machine learning", "ml_pipeline"),
        ("deep learning", "neural_network"),
        ("neural network", "neural_network"),
        ("ann", "neural_network")
    ]
    for needle, label in mapping:
        if needle in lowered:
            return label
    return "generic"


LOCAL_ARCHITECTURE_TEMPLATES = {
    "transformer": {
        "title": "Transformer Architecture",
        "explanation": "A transformer first turns words into embeddings, adds positional information, then uses stacked self-attention and feed-forward blocks to understand relationships between tokens before producing the output.",
        "mermaid": """flowchart TD
Input[Input Tokens] --> Embed[Token Embeddings]
Embed --> Pos[Positional Encoding]
Pos --> Attn[Multi-Head Self-Attention]
Attn --> Add1[Add and Normalize]
Add1 --> FFN[Feed Forward Network]
FFN --> Add2[Add and Normalize]
Add2 --> Stack[Repeat Encoder/Decoder Blocks]
Stack --> Output[Predicted Output Tokens]"""
    },
    "cnn": {
        "title": "CNN Architecture",
        "explanation": "A CNN reads an image, applies convolution filters to detect patterns, reduces size with pooling, and then uses dense layers to classify the final image.",
        "mermaid": """flowchart TD
Image[Input Image] --> Conv1[Convolution Layer]
Conv1 --> Relu1[ReLU Activation]
Relu1 --> Pool1[Pooling Layer]
Pool1 --> Conv2[Deeper Convolution Layer]
Conv2 --> Pool2[Pooling Layer]
Pool2 --> Flat[Flatten]
Flat --> Dense[Dense Layer]
Dense --> Class[Classification Output]"""
    },
    "rnn": {
        "title": "RNN / LSTM Architecture",
        "explanation": "An RNN or LSTM reads sequence elements one by one, keeps a memory of past information, and uses that evolving hidden state to predict the next output.",
        "mermaid": """flowchart LR
X1[Input t1] --> Cell1[RNN/LSTM Cell]
Cell1 --> H1[Hidden State t1]
X2[Input t2] --> Cell2[RNN/LSTM Cell]
H1 --> Cell2
Cell2 --> H2[Hidden State t2]
X3[Input t3] --> Cell3[RNN/LSTM Cell]
H2 --> Cell3
Cell3 --> H3[Hidden State t3]
H3 --> Y[Sequence Output]"""
    },
    "ml_pipeline": {
        "title": "Machine Learning Pipeline",
        "explanation": "A machine learning pipeline starts with data collection and cleaning, then trains a model, evaluates it, and finally deploys it for predictions.",
        "mermaid": """flowchart TD
Data[Collect Data] --> Prep[Clean and Prepare Data]
Prep --> Features[Feature Engineering]
Features --> Train[Train Model]
Train --> Eval[Evaluate Model]
Eval --> Deploy[Deploy Model]
Deploy --> Predict[Make Predictions]"""
    },
    "nlp_pipeline": {
        "title": "NLP Pipeline",
        "explanation": "An NLP system takes text, tokenizes and cleans it, converts it into embeddings or features, processes it with a language model, and then produces a language task output.",
        "mermaid": """flowchart TD
Text[Input Text] --> Clean[Clean and Normalize Text]
Clean --> Tokenize[Tokenization]
Tokenize --> Embed[Embeddings / Vector Representation]
Embed --> Model[Language Model]
Model --> Task[Classification / Translation / Generation]
Task --> Output[Final Output]"""
    },
    "neural_network": {
        "title": "Neural Network Architecture",
        "explanation": "A basic neural network takes input features, passes them through hidden layers where patterns are learned, and then produces an output such as a class or value.",
        "mermaid": """flowchart LR
Input[Input Features] --> Hidden1[Hidden Layer 1]
Hidden1 --> Hidden2[Hidden Layer 2]
Hidden2 --> Output[Output Layer]"""
    }
}


def _extract_json(text):
    if not text:
        raise RuntimeError("The model returned an empty response.")

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", text)
        if not match:
            raise RuntimeError("Could not parse architecture response as JSON.")
        return json.loads(match.group(0))


def generate_architecture(topic, student_name="Student"):
    normalized_topic = normalize_topic(topic)
    if normalized_topic in LOCAL_ARCHITECTURE_TEMPLATES:
        return LOCAL_ARCHITECTURE_TEMPLATES[normalized_topic]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI tutor assistant. Return valid JSON only with keys: "
                    "title, explanation, mermaid. "
                    "The explanation must be short, teacher-like, and easy for a student to understand. "
                    "The mermaid value must be a valid Mermaid flowchart using flowchart TD. "
                    "Do not include markdown fences."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Create a simple but technically correct AI architecture diagram for '{topic}' for student {student_name}. "
                    "Focus on the main components and data flow only. Prefer standard textbook structure over creativity."
                )
            }
        ],
        max_tokens=1200
    )

    parsed = _extract_json(response.choices[0].message.content)
    title = parsed.get("title", f"{topic} Architecture").strip()
    explanation = parsed.get("explanation", "").strip()
    mermaid = parsed.get("mermaid", "").strip()

    if not mermaid.startswith("flowchart"):
        mermaid = "flowchart TD\n" + mermaid

    return {
        "title": title,
        "explanation": explanation,
        "mermaid": mermaid
    }

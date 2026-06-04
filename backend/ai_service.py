# backend/ai_service.py
import sys
import os
import base64
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from groq import Groq
from dotenv import load_dotenv
from backend.knowledge_base import AI_KNOWLEDGE_BASE
from backend.tutor_examples import TUTOR_EXAMPLES

load_dotenv(os.path.join(ROOT_DIR, ".env"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found! Check your .env file.")

client = Groq(api_key=GROQ_API_KEY)

GREETING_PATTERN = re.compile(
    r"^\s*(hi|hello|hey|hii|heyy|hola|good morning|good afternoon|good evening)\s*[!.]*\s*$",
    re.IGNORECASE
)

BASIC_CHAT_PATTERN = re.compile(
    r"^\s*(how are you|how r u|how're you|how are u|what's up|whats up|how is it going|how's it going)\s*[?.!]*\s*$",
    re.IGNORECASE
)

AI_TOPIC_KEYWORDS = {
    "ai", "artificial intelligence", "machine learning", "ml", "deep learning", "dl",
    "nlp", "natural language processing", "neural network", "neural networks",
    "computer vision", "data science", "data scientist", "dataset", "datasets",
    "model", "models", "training", "testing", "validation", "evaluation",
    "classification", "regression", "clustering", "supervised learning",
    "unsupervised learning", "reinforcement learning", "transformer", "transformers",
    "llm", "llms", "large language model", "large language models", "token", "tokens",
    "embedding", "embeddings", "prompt", "prompts", "fine tuning", "fine-tuning",
    "overfitting", "underfitting", "gradient descent", "backpropagation", "cnn",
    "rnn", "lstm", "ann", "accuracy", "precision", "recall", "f1 score",
    "confusion matrix", "loss", "loss function", "cross entropy", "entropy",
    "mean squared error", "mse", "mae", "roc", "auc", "bias", "variance",
    "feature", "features", "label", "labels", "optimizer", "optimizers",
    "activation function", "relu", "sigmoid", "softmax", "dropout", "batch size",
    "epoch", "epochs", "inference", "prediction", "predictions", "hyperparameter",
    "learning rate", "transfer learning", "bert", "gpt", "rag", "tf idf",
    "bag of words", "naive bayes", "logistic regression", "ensemble learning",
    "boosting", "anomaly detection", "recommendation system", "time series",
    "data leakage", "class imbalance", "ethics in ai", "fairness", "gan",
    "autoencoder", "resnet", "batch normalization", "layer normalization"
}

CATEGORY_HINTS = {
    "core": "Foundational AI concepts, evaluation ideas, and training basics.",
    "ml": "Classical machine learning algorithms, pipelines, and tabular modeling topics.",
    "dl": "Neural networks, optimization, regularization, and deep learning architectures.",
    "nlp": "Language modeling, tokenization, transformers, embeddings, and text processing.",
    "ds": "Data science workflows, exploratory analysis, practical modeling use cases, and responsible AI.",
    "ops": "Deployment, inference, monitoring, fine-tuning, and production ML operations.",
    "advanced": "Advanced AI topics such as reinforcement learning and specialized reasoning methods."
}

ARCHITECTURE_REQUEST_PATTERN = re.compile(
    r"\b(architecture|diagram|flowchart|workflow|pipeline|system design|block diagram|architechture)\b",
    re.IGNORECASE
)

FOLLOW_UP_PATTERN = re.compile(
    r"\b(more|continue|go on|tell me more|explain more|more about|related to this topic|this topic|that topic|same topic|same concept|elaborate|in detail|details)\b",
    re.IGNORECASE
)

TOPIC_TAG_PATTERN = re.compile(r"\[TOPIC:\s*(.+?)\]", re.IGNORECASE)


def is_greeting_only(text):
    return bool(text and GREETING_PATTERN.match(text))


def is_basic_chat(text):
    return bool(text and BASIC_CHAT_PATTERN.match(text))


def is_ai_related(text):
    if not text:
        return False

    normalized = re.sub(r"[^a-z0-9+\-# ]", " ", text.lower())
    normalized = re.sub(r"\s+", " ", normalized).strip()
    if not normalized:
        return False

    return any(keyword in normalized for keyword in AI_TOPIC_KEYWORDS)


def retrieve_knowledge_context(text, limit=3):
    if not text:
        return []

    normalized = re.sub(r"[^a-z0-9+\-# ]", " ", text.lower())
    normalized = re.sub(r"\s+", " ", normalized).strip()
    if not normalized:
        return []

    query_tokens = set(normalized.split())
    bigrams = {
        f"{tokens[i]} {tokens[i + 1]}"
        for tokens in [normalized.split()]
        for i in range(len(tokens) - 1)
    }

    scored_items = []
    for item in AI_KNOWLEDGE_BASE:
        score = 0
        topic_norm = item["topic"].lower()
        if topic_norm in normalized:
            score += 8
        elif any(part in topic_norm for part in bigrams):
            score += 4
        for alias in item["aliases"]:
            alias_norm = alias.lower()
            if alias_norm in normalized:
                score += 10 + len(alias_norm.split()) * 2
            else:
                alias_tokens = set(alias_norm.split())
                overlap = len(query_tokens & alias_tokens)
                if overlap:
                    score += overlap
                alias_bigrams = {
                    f"{alias_words[i]} {alias_words[i + 1]}"
                    for alias_words in [alias_norm.split()]
                    for i in range(len(alias_words) - 1)
                }
                bigram_overlap = len(bigrams & alias_bigrams)
                if bigram_overlap:
                    score += bigram_overlap * 3
        if item.get("category") and any(token in CATEGORY_HINTS[item["category"]].lower() for token in query_tokens):
            score += 1
        if score > 0:
            scored_items.append((score, item))

    scored_items.sort(key=lambda pair: pair[0], reverse=True)
    selected = []
    used_topics = set()
    for _, item in scored_items:
        if item["topic"] in used_topics:
            continue
        selected.append(item)
        used_topics.add(item["topic"])
        if len(selected) >= limit:
            break
    return selected


def format_knowledge_context(items):
    if not items:
        return ""

    lines = []
    seen_categories = set()
    for item in items:
        lines.append(f"- {item['topic']}: {item['content']}")
        category = item.get("category")
        if category and category not in seen_categories and category in CATEGORY_HINTS:
            lines.append(f"  Category hint: {CATEGORY_HINTS[category]}")
            seen_categories.add(category)
    return "\n".join(lines)


def retrieve_example_guidance(text, limit=2):
    if not text:
        return []

    normalized = re.sub(r"[^a-z0-9+\-# ]", " ", text.lower())
    normalized = re.sub(r"\s+", " ", normalized).strip()
    if not normalized:
        return []

    query_tokens = set(normalized.split())
    bigrams = {
        f"{tokens[i]} {tokens[i + 1]}"
        for tokens in [normalized.split()]
        for i in range(len(tokens) - 1)
    }

    matches = []
    for item in TUTOR_EXAMPLES:
        score = 0
        for alias in item["aliases"]:
            alias_norm = alias.lower()
            if alias_norm in normalized:
                score += 10 + len(alias_norm.split()) * 2
            else:
                overlap = len(query_tokens & set(alias_norm.split()))
                if overlap:
                    score += overlap
                alias_words = alias_norm.split()
                alias_bigrams = {
                    f"{alias_words[i]} {alias_words[i + 1]}"
                    for i in range(len(alias_words) - 1)
                }
                bigram_overlap = len(bigrams & alias_bigrams)
                if bigram_overlap:
                    score += bigram_overlap * 3
        if score > 0:
            matches.append((score, item))

    matches.sort(key=lambda pair: pair[0], reverse=True)
    return [item for _, item in matches[:limit]]


def format_example_guidance(items):
    if not items:
        return ""

    lines = []
    for item in items:
        lines.append(f"- Example topic: {item['question']} | Teaching style: {item['answer_style']}")
    return "\n".join(lines)


def classify_ai_scope(text, history=None):
    if not text:
        return False

    if is_ai_related(text) or retrieve_knowledge_context(text):
        return True

    latest_topic = extract_latest_topic(history or [])
    if latest_topic and is_follow_up_request(text):
        return True

    try:
        prompt = (
            "Decide whether the user's question is related to AI, Machine Learning, Data Science, "
            "Deep Learning, NLP, Neural Networks, model evaluation, optimization, computer vision, "
            "statistics for ML, or closely related AI topics. "
            "Answer only YES or NO.\n\n"
            f"Question: {text}"
        )
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=5,
            temperature=0
        )
        answer = (response.choices[0].message.content or "").strip().upper()
        return answer.startswith("YES")
    except Exception:
        return False


def detect_request_type(text):
    if not text:
        return "text"

    if ARCHITECTURE_REQUEST_PATTERN.search(text):
        return "diagram"

    return "text"


def is_follow_up_request(text):
    return bool(text and FOLLOW_UP_PATTERN.search(text))


def extract_latest_topic(history):
    if not history:
        return None

    for msg in reversed(history):
        if msg.get("role") != "assistant":
            continue
        content = msg.get("content", "")
        match = TOPIC_TAG_PATTERN.search(content)
        if match:
            return match.group(1).strip()

    for msg in reversed(history):
        content = (msg.get("content") or "").strip()
        if content:
            return content[:80]

    return None


def out_of_scope_reply(student_name="Student"):
    return f"That topic is outside my expertise, {student_name}. Please ask me something from AI, ML, NLP, or DL."


def build_system_prompt(student_name="Student"):
    return f"""You are Ms. Aira, a warm and supportive AI tutor teaching {student_name}.

RULES:
1. Only answer questions about AI, Machine Learning, Deep Learning, NLP, Neural Networks,
   Computer Vision, Data Science, model evaluation, optimization, feature engineering,
   training, inference, datasets, and closely related AI topics.
2. If the student sends only a greeting like "hi" or "hello", reply with only a short greeting.
   Example: "Hello, {student_name}!"
3. If the student sends a simple social message like "how are you", reply warmly and briefly.
   Keep it conversational and do not turn it into a lesson.
4. If the student asks about anything outside your expertise, reply with only:
   "{out_of_scope_reply(student_name)}"
   Do not add any extra explanation.
5. For valid AI-topic questions, teach clearly, step by step, and keep a warm tone.
   Explain the concept like a real teacher, not like a textbook.
   Start with a simple meaning, then a short explanation, then one easy example.
   Use natural conversational sentences.
   Use any provided knowledge notes when they are relevant.
   If the student asks a follow-up like "tell me more" or "explain this topic more",
   continue from the existing topic context instead of treating it as a new unrelated question.
6. For valid AI-topic teaching answers only, add a new line at the end in this format:
   [TOPIC: topic name]
7. Do not add a topic tag for greetings, simple social chat, or out-of-scope replies."""


def process_file(file):
    messages_content = ""
    if not file:
        return messages_content

    filename = file.filename.lower()
    file_data = file.read()

    if filename.endswith(".pdf"):
        try:
            import pypdf
            import io

            reader = pypdf.PdfReader(io.BytesIO(file_data))
            pdf_text = "\n".join(page.extract_text() for page in reader.pages)
            messages_content += f"\n[PDF Content]:\n{pdf_text}\n"
        except Exception:
            messages_content += "\n[PDF uploaded but could not be read]\n"

    elif filename.endswith((".png", ".jpg", ".jpeg", ".gif", ".webp")):
        encoded = base64.standard_b64encode(file_data).decode("utf-8")
        ext = filename.split(".")[-1]
        media_types = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "webp": "image/webp"
        }
        media_type = media_types.get(ext, "image/jpeg")
        try:
            vision_res = client.chat.completions.create(
                model="meta-llama/llama-4-scout-17b-16e-instruct",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": f"data:{media_type};base64,{encoded}"}},
                        {"type": "text", "text": "Describe this image focusing on AI or technology concepts."}
                    ]
                }],
                max_tokens=500
            )
            messages_content += f"\n[Image]: {vision_res.choices[0].message.content}\n"
        except Exception:
            messages_content += "\n[Image uploaded]\n"

    return messages_content


def get_ai_response(user_message, history, file=None, student_name="Student"):
    request_type = detect_request_type(user_message)
    latest_topic = extract_latest_topic(history)
    retrieval_text = user_message or ""
    if latest_topic and is_follow_up_request(user_message):
        retrieval_text = f"{user_message} {latest_topic}".strip()

    knowledge_items = retrieve_knowledge_context(retrieval_text, limit=5)
    knowledge_context = format_knowledge_context(knowledge_items)
    example_items = retrieve_example_guidance(retrieval_text, limit=3)
    example_guidance = format_example_guidance(example_items)

    if user_message and is_greeting_only(user_message):
        return f"Hello, {student_name}!"

    if user_message and is_basic_chat(user_message):
        return f"I'm doing well, {student_name}. How are you?"

    if user_message and request_type == "diagram":
        return f"I can help generate a {request_type} for your AI topic, {student_name}."

    is_contextual_follow_up = bool(
        user_message and latest_topic and is_follow_up_request(user_message)
    )

    is_allowed_ai_scope = classify_ai_scope(user_message, history)

    if user_message and not file and not is_allowed_ai_scope and not is_contextual_follow_up:
        return out_of_scope_reply(student_name)

    file_content = process_file(file)

    content = file_content
    if user_message:
        if is_contextual_follow_up:
            content += f"{user_message}\n\nCurrent topic context: {latest_topic}"
        else:
            content += user_message
    elif not content:
        content = "Hello!"
    else:
        content += "\nPlease explain any AI concepts you find in this."

    if knowledge_context:
        content += f"\n\nRelevant knowledge notes:\n{knowledge_context}"
    if example_guidance:
        content += f"\n\nRelevant example guidance:\n{example_guidance}"

    system_prompt = build_system_prompt(student_name)

    groq_messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        if msg["role"] in ["user", "assistant"]:
            groq_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
    groq_messages.append({"role": "user", "content": content})

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=groq_messages,
            max_tokens=2048
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

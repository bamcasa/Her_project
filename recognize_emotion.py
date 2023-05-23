import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification


def sentiment_analysis(text, model_name="SocialSentimentBe/fine_tuned_kobert_sentiment_classification_v2"):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    outputs = model(**inputs)

    sentiment = torch.argmax(outputs.logits, dim=1).item()

    # 기존에 정의된 감정 라벨 업데이트
    sentiment_mapping = {0: "neutral", 1: "positive", 2: "negative"}
    sentiment_label = sentiment_mapping[sentiment]

    return sentiment_label


input_text = "나는 이곳을 좋아해!"
sentiment = sentiment_analysis(input_text)
print(f"The sentiment of the given text is: {sentiment}")

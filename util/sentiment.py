from google.cloud import language_v1

client = language_v1.LanguageServiceClient()


def analyzeSentiment(text):
    document = language_v1.types.Document(
        content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT
    )

    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    return sentiment.score, sentiment.magnitude


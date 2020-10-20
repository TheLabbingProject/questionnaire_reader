# Questionnaire Reader

Simple class to read our "Base Questionnaire", parse some simple values and
visualize the collected data.

To read the data, simply run:

```python

    from questionnaire_reader import QuestionnaireReader

    qr = QuestionnaireReader(path="https://path/to/collected/data.csv")
```

The collected data is now available as `qr.data`.

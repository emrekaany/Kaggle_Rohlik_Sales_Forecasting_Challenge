# Security policy

The verified source and tests are offline. They do not require credentials, download data, train a remote model, or submit to Kaggle.

- Keep Kaggle credentials in the official Kaggle configuration mechanism or environment, never in the repository.
- Do not commit competition data, model artifacts, submissions, local paths, or personal information.
- Treat legacy notebook cells as untrusted until their data access and side effects have been reviewed.

Use GitHub private vulnerability reporting when available. Do not include a live credential or restricted competition data in a public issue.

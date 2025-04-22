
#Event Log Extraction for Process Mining Using Large Language Models

## Overview

### From Prompt to Process: Large Language Model-Assisted Event Log Extraction from Relational Databases

Process mining is a discipline that enables organizations to discover and analyze their work processes. A prerequisite for conducting a process mining initiative is the so-called event log, which is not always readily available. In such cases, extracting an event log involves various time-consuming tasks, such as creating tailor-made structured query language (SQL) scripts to extract an event log from a relational database. With this work, we investigate the use of large language models (LLMs) to support event log extraction, particularly by leveraging LLMs ability to produce SQL scripts.
This web application enables users to upload their own database or choose from sample example database, fostering an intuitive and seamless exploration experience.

Developed by researchers from <strong>Kühne Logistics University</strong>, this tool serves as a solid foundation for event log generation, allowing users to ask targeted questions and receive real-time responses.

---

## Technical Details

### Prerequisites

- **Python Version**: The application requires Python 3.10.15
- **Dependencies**: All required dependencies are listed in the `requirements.txt` file.

### Getting Started

1. Clone the repository to your local machine:
   ```bash
   git clone ...
   cd ...
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python3.10 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   streamlit run app.py
   ```

5. Open the provided local URL in your browser to start using the chatbot.

---

## Input Zip File Structure

When using the application, the user can upload a **ZIP file** containing the dataset in the following structure:

```
example.zip
└── example/
    ├── db/
    │   ├── click.csv
    │   ├── configuration.csv
    │   ├── invoice.csv
    │   ├── order.csv
    │   ├── payment.csv
    │   └── shipment.csv
    │
    ├── results/                      # (This folder can be left empty)
    │
    ├── csv_schema.xlsx              # Excel file describing the database schema
    └── ground-truth-eventlog.csv    # (Optional) Reference event log for evaluation
```

### 📄 `csv_schema.xlsx` Structure

The `csv_schema.xlsx` file describes the structure of the relational database. It should contain a single sheet with the following columns:

| table_name   | column         | data_type | type | target_table | target_column |
|--------------|----------------|-----------|------|---------------|----------------|
| invoice      | id             |           | PK   |               |                |
| invoice      | creation_date  | DATETIME  |      |               |                |
| invoice      | order_id       |           | FK   | order         | id             |
| order        | id             |           | PK   |               |                |
| order        | creation_date  | DATETIME  |      |               |                |
| payment      | id             |           | PK   |               |                |
| payment      | creation_date  | DATETIME  |      |               |                |
| payment      | invoice_id     |           | FK   | invoice       | id             |
| shipment     | id             |           | PK   |               |                |
| shipment     | creation_date  | DATETIME  |      |               |                |
| shipment     | order_id       |           | FK   | order         | id             |
| configuration| id             |           | PK   |               |                |

- **table_name**: Name of the table (corresponds to a file in the `db/` folder)
- **column**: Column name in the table
- **data_type**: (Optional) Data type such as `DATETIME`
- **type**: Use `PK` for primary keys and `FK` for foreign keys
- **target_table** and **target_column**: Only required for foreign keys; indicate which table and column they reference

This structure is used by the application to understand and reconstruct relationships between the data tables.

---

## Cite
```bash
   @inproceedings{stein2024event,
   title={Event Log Extraction for Process Mining Using Large Language Models},
   author={Stein Dani, Vinicius and Dees, Marcus and Leopold, Henrik and Busch, Kiran and Beerepoot, Iris and van der Werf, Jan Martijn EM and Reijers, Hajo A},
   booktitle={International Conference on Cooperative Information Systems},
   pages={56--72},
   year={2024},
   organization={Springer}
   }
```


## Contact

For inquiries or support, please contact:
- **Email**: [kiran.busch@klu.org]



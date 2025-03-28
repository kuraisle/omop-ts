import marimo

__generated_with = "0.11.26"
app = marimo.App(width="medium")


@app.cell
def _():
    import duckdb
    return (duckdb,)


@app.cell
def _(duckdb):
    duckdb.sql(
        """
        CREATE TABLE concept AS
        SELECT concept_id, concept_name
        FROM read_csv('~/Documents/Code/OMOP work/omop-lite/test-data/CONCEPT.csv', delim='\t')"""
    )
    return (concept,)


@app.cell
def _(concept, duckdb):
    duckdb.sql(
        """
        SELECT *
        FROM read_parquet('~/OneDrive - The University of Nottingham/results/bge_embeddings.parquet') e
        JOIN concept ON concept.concept_id = e.concept_id;"""
    ).to_parquet("~/Documents/Code/OMOP work/omop-lite/test-data/embeddings.parquet")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

import marimo

__generated_with = "0.11.26"
app = marimo.App(width="medium")


@app.cell
def _():
    import psycopg as pg
    import pandas as pd
    return pd, pg


@app.cell
def _(pd):
    concept_class = pd.read_csv("vocabs/CONCEPT_CLASS.csv", sep="\t")
    concept_class_ids = concept_class["concept_class_concept_id"].tolist()
    concept_class
    return concept_class, concept_class_ids


@app.cell
def _(pd):
    domain = pd.read_csv("vocabs/DOMAIN.csv", sep="\t")
    domain_ids = domain["domain_concept_id"].tolist()
    domain
    return domain, domain_ids


@app.cell
def _(pd):
    relationship = pd.read_csv("vocabs/RELATIONSHIP.csv", sep="\t")
    relationship_ids = relationship["relationship_concept_id"].tolist()
    relationship
    return relationship, relationship_ids


@app.cell
def _(pd):
    vocabulary = pd.read_csv("vocabs/VOCABULARY.csv", sep="\t")
    vocabulary_ids = vocabulary["vocabulary_concept_id"].tolist()
    vocabulary
    return vocabulary, vocabulary_ids


@app.cell
def _(concept_class_ids, domain_ids, vocabulary_ids):
    extra_concept_ids = {
        *concept_class_ids,
        *domain_ids,
        *vocabulary_ids
    }

    extra_concept_ids
    return (extra_concept_ids,)


@app.cell
def _():
    query = """
    SELECT
        c.concept_id,
        c.concept_name,
        c.domain_id,
        c.vocabulary_id,
        c.concept_class_id,
        c.standard_concept,
        c.concept_code,
        c.valid_start_date,
        c.valid_end_date,
        c.invalid_reason
    FROM cdm.concept c
    WHERE concept_id = %s;
    """
    return (query,)


@app.cell
def _(extra_concept_ids, pg, query):
    connection_uri = "postgres://postgres:password@localhost:5432/omop"

    with pg.connect(connection_uri) as conn:
        with conn.cursor() as cur:
            concepts = []
            for concept_id in extra_concept_ids:
                cur.execute(query, (concept_id,))
                concepts.append(cur.fetchone())

    concepts
    return concept_id, concepts, conn, connection_uri, cur


@app.cell
def _(concepts, pd):
    concept_df = pd.DataFrame(
        {
            "concept_id": [c[0] for c in concepts],
            "concept_name": [c[1] for c in concepts],
            "domain_id": [c[2] for c in concepts],
            "vocabulary_id": [c[3] for c in concepts],
            "concept_class_id": [c[4] for c in concepts],
            "standard_concept": [c[5] for c in concepts],
            "concept_code": [c[6] for c in concepts],
            "valid_start_date": [c[7] for c in concepts],
            "valid_end_date": [c[8] for c in concepts],
            "invalid_reason": [c[9] for c in concepts],
        }
    )

    concept_df
    return (concept_df,)


@app.cell
def _(concept_df):
    concept_df.to_csv("~/Documents/Code/OMOP work/omop-lite/test-data/CONCEPT.csv", sep="\t", mode="a")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()

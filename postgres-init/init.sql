CREATE TABLE IF NOT EXISTS predictions (
    id varchar PRIMARY KEY,
    predicted float,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS prediction_variables (
    id varchar,
    variable_name varchar,
    variable_value varchar,
    model varchar,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

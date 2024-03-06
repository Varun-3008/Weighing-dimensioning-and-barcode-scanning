CREATE TABLE IF NOT EXISTS profiling (
                id UUID PRIMARY KEY,
                barcode VARCHAR(255),
                length_mm FLOAT,
                width_mm FLOAT,
                height_mm FLOAT,
                boxvolume1 FLOAT,
                realvolume1 FLOAT,
                weight_gms FLOAT,
                length_cm FLOAT,
                width_cm FLOAT,
                height_cm FLOAT,
                boxvolume2 FLOAT,
                realvolume2 FLOAT,
                weight_kg FLOAT,
                isbox BOOLEAN,
                timestamp TIMESTAMP
            );
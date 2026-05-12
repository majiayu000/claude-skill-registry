// SOURCE-OF-TRUTH: shared/scripts/coordinator-runtime/lib/validate.mjs. Edit ONLY here; run `node tools/marketplace/shared.mjs sync`

function isPlainObject(value) {
    return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function matchesType(expectedType, value) {
    if (Array.isArray(expectedType)) {
        return expectedType.some(type => matchesType(type, value));
    }
    switch (expectedType) {
        case "object":
            return isPlainObject(value);
        case "array":
            return Array.isArray(value);
        case "string":
            return typeof value === "string";
        case "integer":
            return typeof value === "number" && Number.isInteger(value);
        case "number":
            return typeof value === "number" && Number.isFinite(value);
        case "boolean":
            return typeof value === "boolean";
        case "null":
            return value === null;
        default:
            return true;
    }
}

function validateNode(schema, value, path, errors) {
    if (!schema || typeof schema !== "object") {
        return;
    }

    if (schema.type && !matchesType(schema.type, value)) {
        errors.push({
            instancePath: path,
            message: `must be ${schema.type}`,
        });
        return;
    }

    if (schema.enum && !schema.enum.includes(value)) {
        errors.push({
            instancePath: path,
            message: `must be one of: ${schema.enum.join(", ")}`,
        });
    }

    if (schema.type === "string" && schema.format === "date-time" && typeof value === "string") {
        if (Number.isNaN(Date.parse(value))) {
            errors.push({
                instancePath: path,
                message: "must be a valid date-time string",
            });
        }
    }

    if (schema.type === "string" && typeof value === "string" && typeof schema.minLength === "number") {
        if (value.length < schema.minLength) {
            errors.push({
                instancePath: path,
                message: `must have length >= ${schema.minLength}`,
            });
        }
    }

    if (schema.type === "array" && Array.isArray(value) && typeof schema.minItems === "number") {
        if (value.length < schema.minItems) {
            errors.push({
                instancePath: path,
                message: `must contain at least ${schema.minItems} item(s)`,
            });
        }
    }

    if ((schema.type === "integer" || schema.type === "number") && typeof value === "number" && typeof schema.minimum === "number") {
        if (value < schema.minimum) {
            errors.push({
                instancePath: path,
                message: `must be >= ${schema.minimum}`,
            });
        }
    }

    if (schema.type === "object" && isPlainObject(value)) {
        const properties = schema.properties || {};
        const required = Array.isArray(schema.required) ? schema.required : [];

        for (const key of required) {
            if (!Object.prototype.hasOwnProperty.call(value, key)) {
                errors.push({
                    instancePath: path,
                    message: `missing required property: ${key}`,
                });
            }
        }

        if (schema.additionalProperties === false) {
            for (const key of Object.keys(value)) {
                if (!Object.prototype.hasOwnProperty.call(properties, key)) {
                    errors.push({
                        instancePath: path ? `${path}/${key}` : `/${key}`,
                        message: "additional property is not allowed",
                    });
                }
            }
        }

        for (const [key, propertySchema] of Object.entries(properties)) {
            if (!Object.prototype.hasOwnProperty.call(value, key)) {
                continue;
            }
            const nextPath = path ? `${path}/${key}` : `/${key}`;
            validateNode(propertySchema, value[key], nextPath, errors);
        }
    }

    if (schema.type === "array" && Array.isArray(value) && schema.items) {
        for (let index = 0; index < value.length; index += 1) {
            validateNode(schema.items, value[index], `${path}/${index}`, errors);
        }
    }
}

export function validateSchema(schema, data) {
    const errors = [];
    validateNode(schema, data, "", errors);
    return {
        ok: errors.length === 0,
        errors,
    };
}

export function formatValidationErrors(errors) {
    return (errors || [])
        .map(error => `${error.instancePath || "/"} ${error.message}`.trim())
        .join("; ");
}

export function assertSchema(schema, data, label = "payload") {
    const result = validateSchema(schema, data);
    if (result.ok) {
        return { ok: true };
    }
    return {
        ok: false,
        error: `Invalid ${label}: ${formatValidationErrors(result.errors)}`,
        details: result.errors,
    };
}

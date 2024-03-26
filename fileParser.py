def parseAttributesFile(filepath):
    attributes = {}

    try:
        with open(filepath, 'r') as file:
            for lineNumber, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(":")
                if len(parts) != 2:
                    print(f"Warning: Line {lineNumber} is malfromed, skipping: {line}")
                    continue
                attribute, valuesString = parts
                values = [value.strip() for value in valuesString.split(',') if value.strip()]
                if len(values) != 2:
                    print(f"Warning: Attribute '{attribute}' does not have exactly two values, skipping: {line}")
                    continue
                attributes[attribute.strip()] = values
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return {}
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return {}
    return attributes
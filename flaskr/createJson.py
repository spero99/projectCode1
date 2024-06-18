import json

def write_Json(coded_message, parameters, errors, sha, entropy):

    dictionary = {
        'encoded_message': coded_message,
        'compression_algorithm: fano-shannon'
        'encoding: cyclic'
        'parameters' : parameters,
        'errors' : errors,
        'SHA256' : sha,
        'entropy' :entropy,
    }

    json_object = json.dumps(dictionary, indent=7)

    with open("coded.json", "w") as outfile:
        outfile.write(json_object)
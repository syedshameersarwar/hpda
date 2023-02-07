#!/usr/bin/env python3

import connexion

from swagger_server import encoder


def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Swagger System Metrics - OpenAPI 3.0'}, pythonic_params=True)
    app.run(port=8080, debug=True)


if __name__ == '__main__':
    main()

'''
To add a new API endpoint and data field for the object, the specification 
would need to be updated, the server code re-generated, and the backend 
implementation modified to reflect the changes. The difficulty of this 
change would depend on the complexity of the change and the existing 
codebase.
'''
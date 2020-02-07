from flask_restplus import Api
from flask import Flask, send_from_directory, session
from flask_cors import CORS
from ....conf.Flask.FlaskConfiguration import FlaskConfiguration
from ..APICore import API
from ....util.api.decorators.http import http_logger
from ....service.helpers.security.RandomStringGenerator import RandomStringGenerator
from ....util.ErrorFactory.GeneralErrors import errorStackTrace

class BuildAPI():

    def __init__(self,apiConfig: FlaskConfiguration,apis: [API]):

        # Configuration
        self._api_config=apiConfig
        self._api_config.initialize_config()
        # API Namespace objects
        self._apis: [API]=apis

        # Collection of namespaces
        self._built_api: Api=None
        self._built_app: Flask=None



    def _construct_api(self)->None:
        # Construct API Object
        self._built_api = Api(
            title=self._api_config.title,
            version=self._api_config.version,
            description=self._api_config.description
        )
        self._built_api.errorhandler=self.default_error_handler

        # Add Namespaces to said API object
        self._configure_namespaces()

    def _configure_namespaces(self)->None:
        # Attach namespaces to given Built API
        for api in self._apis:
            self._built_api.add_namespace(
                api.namespace_object)



    def _construct_app(self)->None:

        # Flask Config
        self._built_app = Flask(__name__)
        self._built_app.debug = self._api_config.debug
        self._built_app.env = self._api_config.ENV
        self._built_app.secret_key=RandomStringGenerator.random_string(self._api_config.secret_key_len)

        # Enable CORS
        if self._api_config.cors_enabled:
            CORS(
                self._built_app,
                resources=self._api_config.cors_resource_setting,
                supports_credentials=self._api_config.cors_with_creds
            )

        # Add Default Angular Routing
        if self._api_config.angular_client:
            self._add_angular_routes()

    def _add_angular_routes(self):
        @self._built_app.route('/test.html')
        def ang_test_html():
            return ("<html>test</html>")

        @self._built_app.route('/test_file.html')
        def ang_test_html_file():
            return send_from_directory('google_transfer1_0', 'test.html')

        @self._built_app.route('/inline.bundle.js')
        def ang_inline():
            return send_from_directory(self._api_config.angular_client_directory, "inline.bundle.js")

        @self._built_app.route('/main.bundle.js')
        def ang_main_bundle():
            return send_from_directory(self._api_config.angular_client_directory, "main.bundle.js")

        @self._built_app.route('/polyfills.bundle.js')
        def ang_polyfills():
            return send_from_directory(self._api_config.angular_client_directory, "polyfills.bundle.js")

        @self._built_app.route('/scripts.bundle.js')
        def ang_script_bundle():
            return send_from_directory(self._api_config.angular_client_directory, "scripts.bundle.js")

        @self._built_app.route('/styles.bundle.js')
        def ang_style_bundle():
            return send_from_directory(self._api_config.angular_client_directory, "styles.bundle.js")

        @self._built_app.route('/vendor.bundle.js')
        def vendor_bundle():
            return send_from_directory(self._api_config.angular_client_directory, "vendor.bundle.js")

        @self._built_app.route('/favicon.ico')
        def favicon():
            return send_from_directory(self._api_config.angular_client_directory, "favicon.ico")

        @self._built_app.route(f'/client/v{self._api_config.version}')
        @http_logger
        def client():
            return send_from_directory(self._api_config.angular_client_directory, "index.html")

        @self._built_app.route(f'/client/v{self._api_config.version}/<path:path>')
        @http_logger
        def client_dynamo(path):
            return send_from_directory(self._api_config.angular_client_directory, "index.html")

        @self._built_app.route('/assets/<path:path>')
        def assets(path):
            return send_from_directory(f"{self._api_config.angular_client_directory}/assets", (str(path)))

    def default_error_handler(self, error):
        """Default error handler"""
        if self._api_config.dev_mode_enabled is True:
            return {'message': 'Internal Server Error.\nStack Trace:\n{errorStackTrace(error)}'}, 500
        else:
            return {'message': 'Internal Server Error'}, 500

    def build(self,build_and_run=True)->None:

        # Build out API Object
        self._construct_api()

        # Build out Flask App Reference
        self._construct_app()

        if build_and_run:
            self.run()

    def run(self)->None:
        # Initialize Namespaces
        self._built_api.init_app(self._built_app)

        # Run on port
        self._built_app.run()
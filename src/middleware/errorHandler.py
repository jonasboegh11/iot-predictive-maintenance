from flask import jsonify

def register_error_handlers(app):
    
    @app.errorhandler(404)
    def not_found(err):
        return jsonify({"error": "Route ikke fundet"}), 404

    @app.errorhandler(500)
    def server_error(err):
        return jsonify({"error": "Noget gik galt på serveren"}), 500

    @app.errorhandler(400)
    def bad_request(err):
        return jsonify({"error": "Ugyldigt request"}), 400
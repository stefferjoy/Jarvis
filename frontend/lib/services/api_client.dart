import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiException implements Exception {
  final String message;
  ApiException(this.message);

  @override
  String toString() => message;
}

class ApiClient {
  ApiClient({this.baseUrl = 'http://localhost:8000'});

  final String baseUrl;

  Future<String> sendChat(String message) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/chat'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'message': message}),
      );

      if (response.statusCode != 200) {
        throw ApiException('Backend error: HTTP ${response.statusCode}.');
      }

      final body = jsonDecode(response.body) as Map<String, dynamic>;
      final reply = body['reply'] as String?;
      if (reply == null || reply.trim().isEmpty) {
        throw ApiException('Backend returned an empty reply.');
      }

      return reply;
    } on ApiException {
      rethrow;
    } catch (_) {
      throw ApiException('Could not reach backend. Check that backend is running.');
    }
  }
}

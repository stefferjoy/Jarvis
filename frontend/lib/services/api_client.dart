import 'dart:convert';

import 'package:http/http.dart' as http;

class ApiClient {
  ApiClient({this.baseUrl = 'http://localhost:8000'});

  final String baseUrl;

  Future<String> sendChat(String message) async {
    final response = await http.post(
      Uri.parse('$baseUrl/chat'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode({'message': message}),
    );

    if (response.statusCode != 200) {
      return 'Backend error: ${response.statusCode}';
    }

    final body = jsonDecode(response.body) as Map<String, dynamic>;
    return (body['reply'] as String?) ?? 'No reply';
  }
}

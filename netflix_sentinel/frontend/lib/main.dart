import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'dashboard.dart';

void main() {
  runApp(const ProviderScope(child: SentinelApp()));
}

class SentinelApp extends StatelessWidget {
  const SentinelApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sentinel IDP',
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF141414), // Dark cinematic aesthetic
        colorScheme: const ColorScheme.dark(primary: Color(0xFFE50914)),
      ),
      home: const DashboardScreen(),
    );
  }
}
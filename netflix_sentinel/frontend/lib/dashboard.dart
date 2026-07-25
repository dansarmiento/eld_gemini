import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

final traceProvider = FutureProvider<List<dynamic>>((ref) async {
  // Simulating the dynamic response by reading the exported backend trace
  final String response = await rootBundle.loadString('assets/incident_trace.json');
  return json.decode(response);
});

class DashboardScreen extends ConsumerWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final tracesAsyncValue = ref.watch(traceProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Sentinel: Ops Orchestrator'),
        backgroundColor: Colors.black,
      ),
      body: tracesAsyncValue.when(
        data: (traces) => ListView.builder(
          padding: const EdgeInsets.all(24.0),
          itemCount: traces.length,
          itemBuilder: (context, index) {
            final trace = traces[index];
            return Card(
              margin: const EdgeInsets.only(bottom: 16.0),
              color: const Color(0xFF2B2B2B),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        const Icon(Icons.hub, color: Color(0xFFE50914)),
                        const SizedBox(width: 8),
                        Text(
                          trace['agent'],
                          style: const TextStyle(
                            fontWeight: FontWeight.bold,
                            fontSize: 18,
                            color: Colors.white,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    Text(
                      trace['action'],
                      style: const TextStyle(
                        fontFamily: 'monospace',
                        color: Colors.white70,
                      ),
                    ),
                  ],
                ),
              ),
            );
          },
        ),
        loading: () => const Center(child: CircularProgressIndicator()),
        error: (err, stack) => Center(child: Text('Error: $err')),
      ),
    );
  }
}
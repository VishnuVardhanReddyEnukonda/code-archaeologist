"use client";

import React, { useEffect, useState } from 'react';
import ReactFlow, { 
  Background, 
  Controls, 
  useNodesState, 
  useEdgesState,
  Node
} from 'reactflow';
import 'reactflow/dist/style.css';

export default function GraphView() {
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  
  // New State: Track which node is clicked
  const [selectedNode, setSelectedNode] = useState<any>(null);

  useEffect(() => {
    fetch('http://localhost:8000/graph')
      .then((res) => res.json())
      .then((data) => {
        const spacedNodes = data.nodes.map((node: any) => {
          const label = node.data.label || "Unknown Node";
          return {
            ...node,
            position: { x: Math.random() * 600, y: Math.random() * 400 },
            data: { 
                label: label, 
                code: node.data.code, 
                explanation: node.data.explanation 
            },
            style: { 
              background: label.includes('.py') ? '#efefef' : '#dcfce7',
              border: '1px solid #777',
              borderRadius: '8px',
              padding: '10px',
              width: 180,
              fontSize: '12px',
              fontWeight: 'bold',
              textAlign: 'center'
            }
          };
        });
        setNodes(spacedNodes);
        setEdges(data.edges);
      })
      .catch((err) => console.error("Failed to fetch graph:", err));
  }, []);

  // Handler: When a user clicks a node
  const onNodeClick = (event: any, node: Node) => {
    setSelectedNode(node.data);
  };

  return (
    <div className="relative w-full h-[600px] border border-gray-200 rounded-lg shadow-lg bg-white overflow-hidden">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={onNodeClick} // <--- Listen for clicks
        fitView
      >
        <Background gap={20} color="#f1f1f1" />
        <Controls />
      </ReactFlow>

      {/* The Inspector Panel (Popup) */}
      {/* The Inspector Panel (Popup) */}
      {selectedNode && (
        <div className="absolute top-4 right-4 w-96 bg-white shadow-2xl border border-gray-200 rounded-xl p-5 z-50 overflow-y-auto max-h-[650px] flex flex-col gap-4">
          
          {/* Header */}
          <div className="flex justify-between items-center border-b pb-2">
            <h3 className="text-lg font-bold text-gray-800 break-words">{selectedNode.label}</h3>
            <button 
                onClick={() => setSelectedNode(null)}
                className="text-gray-400 hover:text-red-500 font-bold"
            >✕</button>
          </div>

          {/* AI Analysis */}
          <div className="bg-blue-50 p-3 rounded-lg border border-blue-100">
            <h4 className="text-xs font-bold uppercase text-blue-500 mb-1">Current Logic</h4>
            <p className="text-sm text-gray-700 italic">
                {selectedNode.explanation || "No analysis available."}
            </p>
          </div>

          {/* Original Code */}
          <div>
            <h4 className="text-xs font-bold uppercase text-gray-400 mb-1">Legacy Code (Python 2.x)</h4>
            <pre className="text-xs bg-gray-100 text-gray-800 p-3 rounded-lg overflow-x-auto font-mono border">
                {selectedNode.code || "No code content."}
            </pre>
          </div>

          {/* Refactor Button Logic */}
          <RefactorSection code={selectedNode.code} />

        </div>
      )}
    </div>
  );
}
function RefactorSection({ code }: { code: string }) {
  const [loadingRefactor, setLoadingRefactor] = useState(false);
  const [loadingTests, setLoadingTests] = useState(false);
  
  const [newCode, setNewCode] = useState("");
  const [testCode, setTestCode] = useState("");

  const handleRefactor = async () => {
    setLoadingRefactor(true);
    try {
      const res = await fetch("http://localhost:8000/refactor", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      const data = await res.json();
      setNewCode(data.refactored_code);
    } catch (e) {
      console.error(e);
    }
    setLoadingRefactor(false);
  };

  const handleGenerateTests = async () => {
    setLoadingTests(true);
    try {
      const res = await fetch("http://localhost:8000/generate-tests", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }), // Sending the ORIGINAL code to generate tests against
      });
      const data = await res.json();
      setTestCode(data.test_code);
    } catch (e) {
      console.error(e);
    }
    setLoadingTests(false);
  };

  return (
    <div className="border-t pt-4 mt-2 flex flex-col gap-3">
      
      {/* --- REFACTOR BUTTON --- */}
      {!newCode ? (
        <button 
          onClick={handleRefactor}
          disabled={loadingRefactor}
          className="w-full py-2 bg-blue-600 text-white rounded-lg font-bold hover:bg-blue-700 transition-all disabled:opacity-50 text-xs"
        >
          {loadingRefactor ? "Refactoring..." : "✨ Auto-Refactor to Python 3"}
        </button>
      ) : (
        <div className="animate-in fade-in zoom-in duration-300">
          <h4 className="text-xs font-bold uppercase text-green-600 mb-1">✅ Modernized Code</h4>
          <pre className="text-xs bg-gray-900 text-green-400 p-3 rounded-lg overflow-x-auto font-mono">
            {newCode}
          </pre>
        </div>
      )}

      {/* --- TEST BUTTON --- */}
      {!testCode ? (
        <button 
          onClick={handleGenerateTests}
          disabled={loadingTests}
          className="w-full py-2 bg-purple-600 text-white rounded-lg font-bold hover:bg-purple-700 transition-all disabled:opacity-50 text-xs"
        >
          {loadingTests ? "Writing Tests..." : "🧪 Generate Unit Tests"}
        </button>
      ) : (
        <div className="animate-in fade-in zoom-in duration-300 mt-2">
          <h4 className="text-xs font-bold uppercase text-purple-600 mb-1">🛡️ Unit Test Suite</h4>
          <pre className="text-xs bg-gray-900 text-purple-300 p-3 rounded-lg overflow-x-auto font-mono">
            {testCode}
          </pre>
        </div>
      )}

      {/* Reset Button */}
      {(newCode || testCode) && (
        <button 
          onClick={() => { setNewCode(""); setTestCode(""); }}
          className="text-xs text-gray-500 underline text-center mt-2"
        >
          Reset All
        </button>
      )}

    </div>
  );
}
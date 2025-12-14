import GraphView from "@/components/GraphView";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-10 bg-gray-50">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm lg:flex mb-8">
        <h1 className="text-4xl font-bold text-blue-600">The Code Archaeologist</h1>
        <p className="text-gray-600">AI-Powered Legacy Migration</p>
      </div>

      {/* The Graph Window */}
      <GraphView />
      
      <div className="mt-8 grid text-center lg:max-w-5xl lg:w-full lg:grid-cols-3 lg:text-left gap-4">
        <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100">
          <h2 className={`mb-3 text-2xl font-semibold`}>Ingest 🚀</h2>
          <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
            Upload legacy code and let Gemini parse the AST.
          </p>
        </div>
        
        <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100">
          <h2 className={`mb-3 text-2xl font-semibold`}>Visualize 🕸️</h2>
          <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
            See dependencies and hidden logic traps.
          </p>
        </div>

        <div className="group rounded-lg border border-transparent px-5 py-4 transition-colors hover:border-gray-300 hover:bg-gray-100">
          <h2 className={`mb-3 text-2xl font-semibold`}>Refactor ⚡</h2>
          <p className={`m-0 max-w-[30ch] text-sm opacity-50`}>
            Auto-generate Python 3 code with Unit Tests.
          </p>
        </div>
      </div>
    </main>
  );
}
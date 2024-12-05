import ghidra.app.decompiler.*;
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import java.io.*;

public class ExportCode extends GhidraScript {

    @Override
    public void run() throws Exception {
        if (getScriptArgs().length < 1) {
            printerr("Usage: ExportCode <output_directory>");
            return;
        }

        String outputDir = getScriptArgs()[0];
        File outDir = new File(outputDir);
        if (!outDir.exists()) {
            outDir.mkdirs();
        }

        // Decompile and export C code
        exportDecompiledCode(outputDir);

        // Export assembly code
        exportAssemblyCode(outputDir);
    }

    private void exportDecompiledCode(String outputDir) throws Exception {
        DecompInterface decomp = new DecompInterface();
        decomp.openProgram(currentProgram);

        FunctionIterator functions = currentProgram.getFunctionManager().getFunctions(true);
        StringBuilder decompiledCode = new StringBuilder();

        for (Function func : functions) {
            DecompileResults results = decomp.decompileFunction(func, 60, monitor);
            if (results.decompileCompleted()) {
                String code = results.getDecompiledFunction().getC();
                decompiledCode.append(code).append("\n");
            }
        }

        // Save decompiled C code to file
        String cOutputPath = outputDir + "/" + currentProgram.getName() + ".c";
        try (PrintWriter out = new PrintWriter(cOutputPath)) {
            out.println(decompiledCode.toString());
        }
    }

    private void exportAssemblyCode(String outputDir) throws IOException {
        Listing listing = currentProgram.getListing();
        InstructionIterator instructions = listing.getInstructions(true);
        StringBuilder assemblyCode = new StringBuilder();

        for (Instruction instr : instructions) {
            assemblyCode.append(instr.toString()).append("\n");
        }

        // Save assembly code to file
        String asmOutputPath = outputDir + "/" + currentProgram.getName() + ".asm";
        try (PrintWriter out = new PrintWriter(asmOutputPath)) {
            out.println(assemblyCode.toString());
        }
    }
}

Current Status: Non-Functional (Critical Bug)
The solver is NOT currently functional and fails to find solutions for most puzzles, including mad_1.bff.

The project has a functional .bff parser , correct data models, and a complete search algorithm . However, the core of the project is non-functional due to a critical bug in the laser physics simulation.


Root Cause: The trace_all_rays function in lazor_solver.py (and lazor_core/solver.py ) incorrectly calculates the path of a refracted laser.

Bug Details: When a laser hits a Refract (C) block, the code correctly allows the original ray to pass through. However, the new reflected ray that should be created is spawned from the laser's previous position (x, y) .

Correct Behavior: The new reflected ray should be spawned from the actual point of impact on the block's boundary (e.g., (nx, ny) for a corner hit or (nx, y) for a vertical wall hit).

Impact: This bug causes the laser path to be incorrect for all puzzles involving refraction, making it impossible for the solver to find a valid solution for mad_1.bff or any other puzzle requiring 'C' blocks.

How to Run
The main executable script is lazor_solver.py .

Navigate to the project directory (example path from docs):



cd '/Users/tommyboy/Desktop/lazor project/lazor_stage2_vscode_bundle (1)'
Run the solver using the following command format:



python lazor_solver.py -i <input_file.bff> -o <output_file.sol> [--diagnose]


Example (testing mad_1.bff):



python lazor_solver.py -i examples/official/mad_1.bff -o out/mad_1.sol --diagnose

Next Steps

CRITICAL: Fix the trace_all_rays function in lazor_solver.py . The rays.append(...) calls within the cell == 'C' conditions must be modified to use the correct collision coordinates (e.g., (nx, ny), (nx, y), (x, ny)) as the spawn point, not (x, y).

Validate: Once fixed, run the solver against mad_1.bff and tiny_5.bff to confirm the physics engine is correct.

Test: Run the solver against all provided test files (mad_4, mad_7, yarn_5, etc.) to ensure all solutions are found correctly.

Performance: Benchmark the solver to ensure it meets the "not slow" requirement (under 2 minutes per board). If it is too slow, the place_and_solve function  will need to be optimized from a simple combination search to a more efficient backtracking algorithm.

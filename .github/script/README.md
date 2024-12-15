# Documentation compile_content.py

## Overview
The compile_content.py script is designed to update markdown files with taxonomie tags, generate reports, and optionally run tests. 
It processes markdown files from a source directory, updates them based on a dataset, and saves the updated files and reports to a destination directory.

## Command Line Arguments
The script accepts the following command line arguments:
- `--dataset`: The path to the dataset file (XLSX file). (Required)
- `--testing`: Determines if it should only check test cases. (Optional)

## Functions
### main()
The main entry point of the script. It performs the following steps:
1. Parses command line arguments.
2. Resolves the source and destination directories.
3. Sets the global VERBOSE and Testing flags based on the arguments.
4. Fills the reports with the dataset information by calling `parseDatasetFile`, `populateRapport1` and `populateRapport2`
5. If the `--testing` flag is set, it runs the test cases and evaluates the results.
6. If the `--testing` flag is not set, it deletes everything in the destination folder, parses the markdown files, populates the image report, and generates the final report.

### parseDatasetFile(dataset_file)
Parses the dataset file from an XLSX file to a list.

### parseMarkdownFiles(src_dir, dest_dir)
Updates markdown files in the source directory with taxonomie tags and generates reports.

### populateRapport1()
Fills the Rapport 1 data with the data from the dataset.

### populateRapport2()
Fills the Rapport 2 data with the data from the dataset.

### populate_image_report(src_dir, dest_dir)
Populates the image report with data from the images in the folders.

### generateReport() 
Generates the final report based on the taxonomie report, success, and failed reports.

### run_test_cases(TEST_DIR)
Runs the functions to test the pipeline.

### test_link_file(TEST_DIR)
Tests the file with incorrect links. This check makes sure incorrect links get noticed and "content/" gets filtered out.

### evaluate_tests(src_dir, dest_dir)
Evaluates the test results.

## Example Usage

```sh
python .github/compile_content.py --src "./content" --dest "./build" --dataset .github/datasets/dataset.xlsx --verbose
```

This command will process the markdown files in the content directory, update them based on the dataset in `./datasets/dataset.xlsx`, and save the updated files and reports to the build directory with verbose output.

## Execution Time
The script prints the total execution time at the end of the run.

```sh
Execution time: 2.34 seconds
```

```mermaid
flowchart TD
    A[Start] --> B[Parse Command Line Arguments]
    B --> C[Resolve Source and Destination Directories]
    C --> D[Set VERBOSE and Testing Flags]
    D --> E[Parse Dataset File]
    E --> F[Populate Rapport 1]
    F --> G[Populate Rapport 2]
    
    G --> H{Testing Flag Set?}
    H -->|Yes| I[Run Test Cases]
    I --> J{Test Cases Successful?}
    J -->|Yes| K[Test Link File]
    K --> L{Test Links Successful?}
    L -->|Yes| M[Evaluate Tests]
    M --> N{Test Evaluation Successful?}
    N -->|Yes| O[Exit with Code 0]
    N -->|No| P[Exit with Code 1]
    L -->|No| Q[Print Changing of dynamic links tests: Failed]
    Q --> P
    J -->|No| R[Print Markdown tests: Failed]
    R --> P
    
    H -->|No| S[Delete Everything in Destination Folder]
    S --> T[Parse Markdown Files]
    T --> U[Populate Image Report]
    U --> V[Generate Report]
    V --> W[End]

    O --> W
    P --> W

    subgraph Parse Markdown Files
        T --> T1[Initialize Destination Directory]
        T1 --> T2[Process Each Markdown File]
        T2 --> T3[Skip 'schrijfwijze' Folder]
        T3 --> T4[Read File Content]
        T4 --> T5[Update Dynamic Links]
        T5 --> T6[Copy Images]
        T6 --> T7[Extract Metadata]
        T7 --> T8[Generate Tags]
        T8 --> T9[Find To-Do Items]
        T9 --> T10[Combine Errors]
        T10 --> T11{Errors Found?}
        T11 -->|Yes| T12[Add to Failed Files]
        T11 -->|No| T13[Add to Successful Files]
        T12 --> T14[Create New Content with Updated Tags]
        T13 --> T14
        T14 --> T15[Write New Content to Destination File]
        T15 --> T16[Print File Completed]
    end
```
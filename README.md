HOME SCREEN:
Run the code through main.py, and a screen should pop up that displays START and QUIT. Clicking QUIT will exit the program.
Clicking START will bring you to the Data Input screen.

DATA INPNUT SCREEN:
Has "Number of Items" which is the number of items that need to be packaged being between 100,000 and 500,000 inclusive, 
"Max Weight" which is the maximum weight of the items being at least 1, and weights are assigned by a weight-generating algorithm in the main file: generate_uneven_distribution.
"Bin Capacity" which is the total weight that a bin can hold, it must be greater than or equal to "Max Weight".
If any of these conditions are not followed, the window will display error messages.

RESULTS SCREEN:
Displays average time and bins used for both algorithms over 5 trials given previous data.
The time and bin ratio are the ratios between the average time and bins used over the runs of First and Next Fit.
Double-clicking on the run buttons on each side will display the specific time and bins used for that trial.
Clicking RESTART will send the USER back to the HOME SCREEN.

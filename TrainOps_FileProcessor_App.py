from tkinter import filedialog
from tkinter import *
import os
import pandas as pd
import glob


root= Tk()
root.title('TrainOps Simulation Files Processing Engine')


e= Entry(root, width=50)
e.grid(row=1, column=2, columnspan=15)

e.insert(0,show="Enter File Name Pattern")

def func_file_process(listScenarios, FileNamePattren):

    finalList = []
    for f in listScenarios:
        os.chdir("./" + f)
        # print('Current Dir: ' , os.getcwd())
        Files = [f for f in glob.glob(FileNamePattren)]
        ListByScenario = []
        for i in Files:
            raw_data = pd.read_table(i, sep="\t", skiprows=6)
            raw_data['scenario'] = f.replace("/", "")
            print(raw_data.head(1))
            ListByScenario.append(raw_data)

        DfByScenario = pd.concat(ListByScenario, axis=0, ignore_index=True)
        finalList.append(DfByScenario)
        path_parent = os.path.dirname(os.getcwd())
        os.chdir(path_parent)
        # print('Current Dir: ' , os.getcwd())
    DfAll = pd.concat(finalList, axis=0, ignore_index=True)


    Feeder_grp = DfAll.groupby(['Feeder'])
    max_peak_df = Feeder_grp['Peak'].max().to_frame()
    max_15min_df = Feeder_grp['15 Minutes'].max().to_frame()
    all_peak_df = pd.merge(max_peak_df, DfAll,
                           on=['Peak', 'Feeder'], how='left').drop(['15 Minutes'], axis=1)

    all_max_15min_df = pd.merge(max_15min_df, DfAll,
                                on=['15 Minutes', 'Feeder'], how='left').drop(['Peak'], axis=1)

    final_df = pd.merge(all_peak_df, all_max_15min_df, on=['Feeder'],
                        how='inner', suffixes=('_Peak', '_15_Mins'))

    final_df = final_df[['Feeder', 'Peak', 'scenario_Peak', '15 Minutes', 'scenario_15_Mins']]

    final_df.to_csv("Negfeed_summary_reports.csv", index=False)




def folder_selection():
    folder_selected=filedialog.askdirectory()
    os.chdir(folder_selected)
    print(os.getcwd())

    listScenarios = glob.glob('*/')
    for j in listScenarios:
        print(j)

    print(len(listScenarios))


    myLabel = Label(root, text=folder_selected)
    myLabel.grid(row=4, column=1, padx=20, pady=10, columnspan=15)

    myLabel1 = Label(root, text="No. of Folders: " + str(len(listScenarios)))
    myLabel1.grid(row=5, column=1, padx=20, pady=10, columnspan=15)

    func_file_process(listScenarios, e.get())


myButton = Button(root, text="Select Parent Directory", padx=10, pady=20,
                   command=folder_selection, fg="blue", bg="white")

myButton.grid(row=2, column=1, columnspan=15)

root.mainloop()
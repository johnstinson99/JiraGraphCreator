import pandas as pd
from os.path import join
from App.Code.Views_Seaborn.seaborn_analysis import SeabornGenerator
from App.Code.Jira_DF_Reader.jira_df_reader import JiraDFReader

my_source_path = 'C:\\Users\\John\\Documents\\2016\\Python\\JiraStates'

#my_output_path = 'C:\\Users\\John\\Documents\\Visual Studio 2013\\Projects\\DirectedGraph4\\CrosswordViewer\\seaborne_images'
my_csv_file_and_path = join(my_source_path, 'jira_states.csv')
# jira_df = pd.read_csv(my_csv_file_and_path)
my_jira_df_reader = JiraDFReader(my_csv_file_and_path)
jira_df = my_jira_df_reader.get_final_df()
# print(jira_df)

my_root_output_path = 'C:\\Users\\John\\Documents\\Visual Studio 2013\\Projects\\DirectedGraph4\\CrosswordViewer'
my_relative_output_path = 'seaborne_images'
my_seaborn_gen = SeabornGenerator(my_root_output_path, my_relative_output_path, jira_df)
my_list = my_seaborn_gen.get_png_list()
# my_seaborn_gen.open_files_in_chrome(my_list)
# print("my_dict = " + str(my_list))
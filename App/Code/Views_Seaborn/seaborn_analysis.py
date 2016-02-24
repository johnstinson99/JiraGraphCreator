
import matplotlib.pyplot as plt
from os.path import join
from os import system
import seaborn as sns


class SeabornGenerator:
    def __init__(self, my_path, my_jira_df):
        self.filename_dict = {}
        self.path = my_path
        self.jira_df = my_jira_df
        self.set_style()
        # print("jira_df = ")
        # print(str(self.jira_df))
        print("my_path = ")
        print(self.path)

        # my_dir = 'C:\\Users\\John\\Documents\\2016\\Python\\JiraStates'
        self.plot_graph1(self.jira_df, "output1", "title output1", self.path, self.filename_dict)
        self.plot_facet_grid(self.jira_df, "facet_grid", "state transition time analysis facet grid from seaborne", self.path, self.filename_dict)
        self.plot_graph3(self.jira_df, "output3", "title output3", self.path, self.filename_dict)
        # self.open_files_in_chrome(self.filename_dict)

    def get_filename_dict(self):
        return self.filename_dict

    # Load JIRA dataframe
    # my_csv_file_and_path = join(my_dir, 'jira_states.csv')
    # jira_df = pd.read_csv(my_csv_file_and_path)
    # print(jira_df)
    def set_style(self):
        sns.set(style="whitegrid", color_codes=True)

    def save_file(self, my_filename_without_path_no_extension, my_chart_title, my_path, my_filename_dict):
        my_file_and_path = join(my_path, my_filename_without_path_no_extension + ".png")
        plt.savefig(my_file_and_path)
        my_dict = {}
        my_dict["file_and_path"] = my_file_and_path
        my_dict["title"] = my_chart_title
        # my_dict["x_pixels"] = 1000
        # my_dict["y_pixels"] = 1000
        my_filename_dict[my_filename_without_path_no_extension] = my_dict

    def plot_graph1(self, my_jira_df, my_filename_without_path, my_chart_title, my_path, my_filename_dict):
        g = sns.PairGrid(my_jira_df, vars=["DayDiff", "DateNum"])  # , hue="IssueType"
        g.map(plt.scatter)
        # print("my_filename_without_path = " + my_filename_without_path)
        # print("my_path = " + my_path)
        # print("my_filename_dict = " + str(my_filename_dict))
        self.save_file(my_filename_without_path, my_chart_title, my_path, my_filename_dict)

    def plot_facet_grid(self, my_jira_df, my_filename_without_path, my_chart_title, my_path, my_filename_dict):
        with sns.axes_style("white"):
            '''g = sns.FacetGrid(
                    my_jira_df,
                    row="IssueType",
                    col="From",
                    margin_titles=True,
                    size=2.5,
                    hue = 'To')'''
            g = sns.FacetGrid(
                    my_jira_df,
                    row="To",
                    col="From",
                    margin_titles=True,
                    size=2.5,
                    hue='IssueType')
            g.map(plt.scatter,
                  "WeekNum",
                  "DayDiff",
                  color="#334488",
                  edgecolor="white",
                  lw=.5)
            g.set_axis_labels("Week Number", "Days in State")
            g.set(xticks=list(range(0, 101, 20)), yticks=list(range(0, 101, 20)))
            g.fig.subplots_adjust(wspace=.02, hspace=.02)

        self.save_file(my_filename_without_path, my_chart_title, my_path, my_filename_dict)

    def plot_graph3(self, my_jira_df, my_filename_without_path, my_chart_title, my_path, my_filename_dict):
        sns.swarmplot(x="From", y="DayDiff", hue="To", data=my_jira_df)
        self.save_file(my_filename_without_path, my_chart_title, my_path, my_filename_dict)

    # print("chrome_file = " + chrome_file)
    # print("png_file = " + my_png_file_and_path)
    # call(["dir"])

    def open_files_in_chrome(self, filename_dict):
        chrome_file = '"c:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"'
        for my_file in filename_dict.values():
            system(chrome_file + " " + my_file)


import matplotlib.pyplot as plt
from os.path import join
from os import system
import seaborn as sns
from PIL import Image


class SeabornGenerator:
    def __init__(self, my_root_output_path, my_relative_output_path, my_jira_df_including_undefined):
        # self.filename_dict = {}
        self.png_list = []
        self.output_path = join(my_root_output_path, my_relative_output_path)
        self.relative_output_path = my_relative_output_path
        # tips[tips['time'] == 'Dinner'].
        self.jira_df = my_jira_df_including_undefined
        self.set_style()
        # print("jira_df = ")
        # print(str(self.jira_df))
        print("my_output_path = ")
        print(self.output_path)
        #         self.jira_df = my_jira_df_including_undefined[my_jira_df_including_undefined['From'] != "Undefined"]

        # my_dir = 'C:\\Users\\John\\Documents\\2016\\Python\\JiraStates'
        self.plot_hours_of_day(self.jira_df, "hours_of_day", "hours of day", self.output_path, self.relative_output_path, self.png_list)
        self.plot_day_date_swarm(self.jira_df, "day_date_swarm", "days and dates swarm", self.output_path, self.relative_output_path, self.png_list)
        self.plot_days_and_dates(self.jira_df, "days_and_dates", "Days amd Dates", self.output_path, self.relative_output_path, self.png_list)
        self.plot_facet_time_on_weekdays(self.jira_df, "time_on_weekdays", "Weekday Time", self.output_path, self.relative_output_path, self.png_list)
        self.plot_facet_grid(self.jira_df, "facet_grid", "state transition time analysis facet grid from seaborne", self.output_path, self.relative_output_path, self.png_list)
       # self.open_files_in_chrome(self.filename_dict)

    def get_png_list(self):
        return self.png_list

    # Load JIRA dataframe
    # my_csv_file_and_path = join(my_dir, 'jira_states.csv')
    # jira_df = pd.read_csv(my_csv_file_and_path)
    # print(jira_df)
    def set_style(self):
        sns.set(style="whitegrid", color_codes=True)

    def save_file(self, my_filename_without_path_no_extension, my_chart_title, my_output_path, my_relative_output_path, my_png_list, my_graph):
        my_file_and_path = join(my_output_path, my_filename_without_path_no_extension + ".png")
        print("my_file_and_path = " + my_file_and_path)
        plt.savefig(my_file_and_path)
        # my_graph.savefig(my_file_and_path)  # AttributeError: 'AxesSubplot' object has no attribute 'savefig'
        pil_image = Image.open(my_file_and_path)
        image_width, image_height = pil_image.size
        print("image_width = " + str(image_width) + "image_height = " + str(image_height))
        my_dict = {}
        my_relative_file_and_path = join(my_relative_output_path, my_filename_without_path_no_extension + ".png")
        my_dict["filename_no_extension"] = my_filename_without_path_no_extension
        my_dict["relative_file_and_path"] = my_relative_file_and_path
        my_dict["title"] = my_chart_title
        my_dict["image_width"] = image_width
        my_dict["image_height"] = image_height
        # my_dict["x_pixels"] = 1000
        # my_dict["y_pixels"] = 1000
        # my_filename_dict[my_filename_without_path_no_extension] = my_dict
        my_png_list.append(my_dict)

    def plot_days_and_dates(self, my_jira_df, my_filename_without_path, my_chart_title, my_output_path, my_relative_output_path, my_png_list):
        # g = sns.PairGrid(my_jira_df, vars=["DayDiff", "DateNum"])  # , hue="IssueType"
        # g.map(plt.scatter)
        g = sns.regplot(data = my_jira_df, x = 'DayDiff', y = 'DateNum')
        g.set( yticks=list(range(100, 1001, 100)))
        # print("my_filename_without_path = " + my_filename_without_path)
        # print("my_filename_dict = " + str(my_filename_dict))
        self.save_file(my_filename_without_path, my_chart_title, my_output_path, my_relative_output_path, my_png_list, g)

    def plot_facet_grid(self, my_jira_df, my_filename_without_path, my_chart_title, my_output_path, my_relative_output_path, my_png_list):
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
            g.set(xticks=list(range(0, 101, 20)), yticks=list(range(0, 1001, 100)))
            g.fig.subplots_adjust(wspace=.02, hspace=.02)

        self.save_file(my_filename_without_path, my_chart_title, my_output_path, my_relative_output_path, my_png_list, g)

    def plot_day_date_swarm(self, my_jira_df, my_filename_without_path, my_chart_title, my_output_path, my_relative_output_path, my_png_list):
        # g = sns.Grid(my_jira_df, vars=["DayDiff", "DateNum"])
        # print("HHHHHHHHHHH")
        g = sns.swarmplot(x="From", y="DayDiff", hue="To", data=my_jira_df)
        g.set( yticks=list(range(100,1001, 100)))
        self.save_file(my_filename_without_path, my_chart_title, my_output_path, my_relative_output_path,  my_png_list, g)

    def plot_hours_of_day(self, my_jira_df, my_filename_without_path, my_chart_title, my_output_path, my_relative_output_path, my_png_list):
        # g = sns.Grid(my_jira_df, vars=["DayDiff", "DateNum"])
        # g = sns.swarmplot(x="From", y="HoursOfDay", hue="To", data=my_jira_df)
        g = sns.swarmplot(x="Project", y="HoursOfDay", hue="StateChange", data=my_jira_df)

        g.set( yticks=list(range(8, 18, 1)))
        # sns.sinplot()
        self.save_file(my_filename_without_path, my_chart_title, my_output_path, my_relative_output_path,  my_png_list, g)

    def plot_facet_time_on_weekdays(self, my_jira_df, my_filename_without_path, my_chart_title, my_output_path, my_relative_output_path, my_png_list):
        # g = sns.Grid(my_jira_df, vars=["DayDiff", "DateNum"])
        # g = sns.swarmplot(x="From", y="HoursOfDay", hue="To", data=my_jira_df)
        # g = sns.swarmplot(x="Project", y="HoursOfDay", hue="StateChange", data=my_jira_df)
        g = sns.FacetGrid(
                my_jira_df,
                col="DayOfWeek",
                margin_titles=True,
                size=2.5,
                hue='StateChange')
        g.map(

                # sns.regplot, "size", "total_bill", color=".3", fit_reg=False, x_jitter=.1);
                sns.swarmplot,
                x="Project",
                y="HoursOfDay",
                hue="StateChange",
                data=my_jira_df
        )
        g.set_axis_labels("TimeHours", "Project")
        #g.set(yticks=list(range(8, 18, 1)))
        # g.set( yticks=list(range(8, 18, 1)))
        # g.set(xticks=list(range(0, 101, 20)), yticks=list(range(0, 1001, 100)))
        g.fig.subplots_adjust(wspace=.02, hspace=.02)

        ## g = sns.swarmplot(x="DayOfWeek", y="HoursOfDay", hue="StateChange", data=my_jira_df)

        g.set( yticks=list(range(8, 18, 1)))
        # sns.sinplot()
        self.save_file(my_filename_without_path, my_chart_title, my_output_path, my_relative_output_path,  my_png_list, g)


    # print("chrome_file = " + chrome_file)
    # print("png_file = " + my_png_file_and_path)
    # call(["dir"])

    def open_files_in_chrome(self, filename_list):
        chrome_file = '"c:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"'
        for my_file in filename_list.values():
            system(chrome_file + " " + my_file)

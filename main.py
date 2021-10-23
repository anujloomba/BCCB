from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.properties import ListProperty, ObjectProperty,StringProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
import pandas as pd
import random
import urllib.request


from kivy.clock import Clock
# import matplotlib.pyplot as plt
from math import floor


no_cap=['Himalaya Parashar','Anuj Loomba','Chandrasekhar Pulapaka','Saurabh Mittal']
np_vice=['Anuj Loomba','Chandrasekhar Pulapaka','Saurabh Mittal']




class Manager(ScreenManager):

    pass

class Screen1(Screen):
    urllib.request.urlretrieve("https://docs.google.com/uc?export=download&id=1GfVxUjJUJYz5taFPgyTegSFAi7q8fLKg",
                               "file.xlsx")
    # urllib.request.urlretrieve("https://docs.google.com/spreadsheets/d/1dTyDDnuFjffk_mvcxxahedBQnUKyRJE_AkMgepREEI8","attendance.xlsx")
    # testfile.retrieve("https://docs.google.com/uc?export=download&id=1GfVxUjJUJYz5taFPgyTegSFAi7q8fLKg", "file.xlsx")
    # data=pd.read_csv('https://docs.google.com/file/d/1GfVxUjJUJYz5taFPgyTegSFAi7q8fLKg/edit?usp=docslist_api&filetype=msexcel?format=xls')
    # attendance_data= pd.read_excel('attendance.xlsx')
    data = pd.read_excel('file.xlsx', sheet_name='CurrentFormStats')[['NAME']]
    data = data[~data['NAME'].isna()].fillna(0)
    drop_values=list(data['NAME'])
    whos_playing=[]
    team1 = []
    team1_txt=''
    team2 = []
    team2_txt=''
    cap1=''
    cap2=''
    avg_1=''
    avg_2=''
    data_grp=pd.DataFrame()
    total_overs_min=0
    total_overs_max = 0
    rec_overs=''
    team1_runs_bowl=''
    team2_runs_bowl = ''


    # print (select_val)
    def calledwithbutton(self):
        self.manager.current = 'second'
        # print(self.whos_playing)
        # self.whos_playing=self.manager.ids.players.whos_playing



    def process_stuff(self):
        self.whos_playing = self.manager.screens[0].whos_playing
        data = pd.read_excel('file.xlsx', sheet_name='BattingStats')[
            ['NAME', 'ACTUAL MEAN (BATTING RUNS)','STANDARD DEVIATION(BATTING RUNS)']]
        # data_runs = pd.read_excel('file.xlsx', sheet_name='BattingStats')[['NAME', 'AVERAGE']]
        data_bowl = pd.read_excel('file.xlsx', sheet_name='BowlingProfile')[['NAME', 'BOWLING PROFILE']]
        data_bowl_stat=pd.read_excel('file.xlsx', sheet_name='BowlingStats')[['NAME', 'ECONOMY RATE','STANDARD DEVIATION(ECONOMY RATE)']]
        data = data[~data['NAME'].isna()].fillna(0)
        data_bowl = data_bowl[~data_bowl['NAME'].isna()].fillna(0)
        data_bowl_stat = data_bowl_stat[~data_bowl_stat['NAME'].isna()].fillna(0)
        data = data.set_index('NAME')
        # data_runs = data_runs.set_index('NAME')
        data_bowl = data_bowl.set_index('NAME')
        data_bowl_stat = data_bowl_stat.set_index('NAME')
        # data = data.join(data_runs)
        data = data.join(data_bowl)
        data = data.join(data_bowl_stat)
        data = data.loc[self.whos_playing, :]
        data = data.rename(columns={'ACTUAL MEAN (BATTING RUNS)': 'AVERAGE',
                                    'BOWLING PROFILE': 'BOWLING',
                                    'STANDARD DEVIATION(BATTING RUNS)': 'Std_bat',
                                    'ECONOMY RATE': 'econ',
                                    'STANDARD DEVIATION(ECONOMY RATE)': 'Std_ball'})
        data['Team'] = 3
        data['overs']= 0
        data['position'] = 'none'
        # Selecting Fast bowlers and assigning random teams!

        # data.loc[(data['BOWLING'] == 'FST') & (
        #         data['AVERAGE'] >= data['AVERAGE BOWLING POINTS'].quantile(.6)), 'position'] = 'All'
        # data.loc[(data['AVERAGE BOWLING POINTS'] >= data[(data['position'] == 'none')][
        #     'AVERAGE BOWLING POINTS'].quantile(.7)) & (data['position'] == 'none'), 'position'] = 'Ball'
        # data.loc[(data['AVERAGE BATTING POINTS'] >= data[(data['position'] == 'none')][
        #     'AVERAGE BATTING POINTS'].quantile(.7)) & (data['position'] == 'none'), 'position'] = 'Bat'

        total_ball = data[data['BOWLING'] == 'FST'].shape[0]
        self.team1 = random.sample(list(data[data['BOWLING'] == 'FST'].index), int(total_ball / 2))
        for item1 in list(data[data['BOWLING'] == 'FST'].index):
            if item1 in self.team1:
                data.loc[data.index == item1, 'Team'] = 1
            else:
                data.loc[data.index == item1, 'Team'] = 2
        # data.loc[data[(data['BOWLING'] == 'FST')].index, 'overs'] = 4
        print (data)
        # total_bat = data[data['BOWLING'] == 'MED'].shape[0]
        # self.team1 = random.sample(list(data[data['BOWLING'] == 'MED'].index), int(total_bat / 2))
        # for item1 in list(data[data['position'] == 'Bat'].index):
        #     if item1 in self.team1:
        #         data.loc[data.index == item1, 'Team'] = 1
        #     else:
        #         data.loc[data.index == item1, 'Team'] = 2

        # We do this till there is no Med bowler assigned to team 3
        # When the gap between any 2 teams become more than the remaining players in team 3, we assign all players to the remaining team
        while data[(data['BOWLING'] == 'MED') & (data['Team'] == 3)].shape[0]>0:
            data_grp = data.groupby('Team')['AVERAGE'].sum().reset_index()
            data['AVERAGE']=pd.to_numeric(data['AVERAGE'])
            add1 = data[(data['BOWLING'] == 'MED') & (data['Team'] == 3)]['AVERAGE'].idxmax()
            # print (add1)
            if data[(data['Team'] == 1)].shape[0]-data[(data['Team'] == 2)].shape[0]>=data[
                (data['BOWLING'] == 'MED') & (data['Team'] == 3)].shape[0]:
                data.loc[data[(data['BOWLING'] == 'MED') & (data['Team'] == 3)].index,'Team']=2
            elif data[(data['Team'] == 2)].shape[0]-data[(data['Team'] == 1)].shape[0]>=data[
                (data['BOWLING'] == 'MED') & (data['Team'] == 3)].shape[0]:
                data.loc[data[(data['BOWLING'] == 'MED') & (data['Team'] == 3)].index,'Team']=1
            elif data_grp.loc[data_grp[data_grp['Team'] == 1].index, 'AVERAGE'].values > data_grp.loc[
                data_grp[data_grp['Team'] == 2].index, 'AVERAGE'].values:
                data.loc[data.index == add1, 'Team'] = 2
            else:
                data.loc[data.index == add1, 'Team'] = 1
                # print(data)
                # print(data_grp)

        while data[(data['BOWLING'] == 'DNB') & (data['Team'] == 3)].shape[0]>0:

            data_grp = data.groupby('Team')['AVERAGE'].sum().reset_index()
            # print(data_grp)
            add1 = data[(data['BOWLING'] == 'DNB') & (data['Team'] == 3)]['AVERAGE'].idxmax()
            if data[(data['Team'] == 1)].shape[0]-data[(data['Team'] == 2)].shape[0]>=data[
                (data['BOWLING'] == 'DNB') & (data['Team'] == 3)].shape[0]:
                data.loc[data[(data['BOWLING'] == 'DNB') & (data['Team'] == 3)].index,'Team']=2
            elif data[(data['Team'] == 2)].shape[0]-data[(data['Team'] == 1)].shape[0]>=data[
                (data['BOWLING'] == 'DNB') & (data['Team'] == 3)].shape[0]:
                data.loc[data[(data['BOWLING'] == 'DNB') & (data['Team'] == 3)].index,'Team']=1
            elif data_grp.loc[data_grp[data_grp['Team'] == 1].index, 'AVERAGE'].values > data_grp.loc[
                data_grp[data_grp['Team'] == 2].index, 'AVERAGE'].values:
                if data[(data['BOWLING'] == 'DNB') &
                        (data['Team'] == 1)].shape[0]-data[(data['BOWLING'] == 'DNB') &
                                                           (data['Team'] == 2)].shape[0]>=1:
                    data.loc[data.index == add1, 'Team'] = 1
                else:
                    data.loc[data.index == add1, 'Team'] = 2
            else:
                if data[(data['BOWLING'] == 'DNB') &
                        (data['Team'] == 2)].shape[0] - data[(data['BOWLING'] == 'DNB') &
                                                             (data['Team'] == 1)].shape[0] >= 1:
                    data.loc[data.index == add1, 'Team'] = 2
                else:
                    data.loc[data.index == add1, 'Team'] = 1

        print(data)
        print(data_grp)

        #Assign over based on bowler type and check the number of overs
        data.loc[data[(data['BOWLING'] == 'MED')].index, 'overs'] = 2
        data.loc[data[(data['BOWLING'] == 'DNB')].index, 'overs'] = 1
        data.loc[data[(data['BOWLING'] == 'FST')].index, 'overs'] = 3
        overs_per_team=data.groupby('Team')['overs'].sum()
        self.total_overs_min=overs_per_team.min()
        data.loc[data[(data['BOWLING'] == 'FST')].index, 'overs'] = 4
        overs_per_team = data.groupby('Team')['overs'].sum()
        self.total_overs_max = overs_per_team.min()
        team_max = overs_per_team.idxmax()

        while overs_per_team.max()!=overs_per_team.min():
            max_overs = data.loc[data[(data['Team']==team_max)].index,'overs'].max()
            bowler_red = data.loc[data[(data['Team']==team_max)&(data['overs']==max_overs)].index,'econ'].idxmax()
            data.loc[bowler_red,'overs']=max_overs-1
            overs_per_team = data.groupby('Team')['overs'].sum()

        data['var_ball']=(data['Std_ball']*data['overs'])**2
        var_ball=(data.groupby('Team')['var_ball'].mean())**0.5
        data['runs_conceded'] = (data['econ']* data['overs'])
        ball_runs=data.groupby('Team')['runs_conceded'].sum()
        self.team1 = list(data[data['Team'] == 1].index)
        self.team2 = list(data[data['Team'] == 2].index)
        data['var_bat'] = (data['Std_bat']) ** 2
        var_bat = (data.groupby('Team')['var_bat'].mean()) ** 0.5
        data['runs_scored'] = (data['AVERAGE'])
        bat_runs = data.groupby('Team')['runs_scored'].sum()


        self.cap1 = "Capt 1: "+ random.choice([x for x in self.team1 if x not in no_cap])
        # cap1 = ''
        # cap2 = ''
        self.cap2 = "Capt 2: "+ random.choice([x for x in self.team2 if x not in no_cap])

        self.team1_txt = str(self.team1)
        self.team2_txt = str(self.team2)
        self.avg_1 = "Expected to score between {min} to {max} runs".format(
            min=int(round((bat_runs - 1.44 * var_bat.loc[1]).loc[1])),
            max=int(round((bat_runs + 1.44 * var_bat.loc[1]).loc[1])))
        self.avg_2 = "Expected to score between {min} to {max} runs".format(
            min=int(round((bat_runs - 1.44 * var_bat.loc[2]).loc[2])),
            max=int(round((bat_runs + 1.44 * var_bat.loc[2]).loc[2])))
        self.rec_overs="Recommended number of overs are between {min} & {max}".format(min=str(self.total_overs_min),max= str(self.total_overs_max))
        self.team1_runs_bowl = "Expected to concede {min} to {max} runs in bowling".format(
            min=int(round((ball_runs-1.44 * var_ball.loc[1]).loc[1])),
            max=int(round((ball_runs+1.44 * var_ball.loc[1]).loc[1])))
        self.team2_runs_bowl = "Expected to concede {min} to {max} runs in bowling".format(
            min=int(round((ball_runs - 1.44 * var_ball.loc[2]).loc[2])),
            max=int(round((ball_runs + 1.44 * var_ball.loc[2]).loc[2])))

class Screen2(Screen):
    whos_playing=[]
    team1 = []
    team1_txt=StringProperty('')
    team2 = []
    team2_txt= StringProperty('')
    cap1=StringProperty('')
    cap2=StringProperty('')
    avg_1 = StringProperty('')
    avg_2 = StringProperty('')
    rec_overs = StringProperty('')
    team1_runs_bowl=StringProperty('')
    team2_runs_bowl = StringProperty('')

    def calledwithbutton(self):
        self.manager.current = 'first'
    def calledwithbuttongif(self):
        self.manager.current = 'gif'
class Screen3(Screen):
    toss = StringProperty('')
    def on_enter(self, *args):
        # print("on Enter")
        Clock.schedule_once(self.callbackfun, 0.5)

    def callbackfun(self,dt):
        self.toss=random.choice(["third","fourth"])
        self.manager.current = self.toss
class Screen4(Screen):

    def callbackfun(self):
        self.manager.current = 'gif'

class Screen5(Screen):

    def callbackfun(self):
        self.manager.current = 'gif'



class MultiSelectSpinners(Button):
    """Widget allowing to select multiple text options."""
    # print(1)
    dropdown = ObjectProperty(None)
    """(internal) DropDown used with MultiSelectSpinner."""

    values = ListProperty([])
    """Values to choose from."""

    selected_values = ListProperty([])
    """List of values selected by the user."""

    whos_playing=[]


    def __init__(self, **kwargs):
        self.bind(dropdown=self.update_dropdown)
        self.bind(values=self.update_dropdown)
        super(MultiSelectSpinners, self).__init__(**kwargs)
        self.bind(on_release=self.toggle_dropdown)


    def toggle_dropdown(self, *args):
        if self.dropdown.parent:
            self.dropdown.dismiss()
        else:
            self.dropdown.open(self)

    def update_dropdown(self, *args):
        if not self.dropdown:
            self.dropdown = DropDown()
        values = self.values
        if values:
            if self.dropdown.children:
                self.dropdown.clear_widgets()
            for value in values:
                b = Factory.MultiSelectOption(text=value+'\n')
                b.bind(state=self.select_value)
                self.dropdown.add_widget(b)



    def select_value(self, instance, value):
        if value == 'down':
            if instance.text not in self.selected_values:
                self.selected_values.append(instance.text)
                self.whos_playing.append(instance.text.replace('\n',''))
        else:
            if instance.text in self.selected_values:
                self.selected_values.remove(instance.text)
                self.whos_playing.remove(instance.text.replace('\n',''))

    def on_selected_values(self, instance, value):
        if value:
            self.text = ', '.join(value)

        else:
            self.text = ''



kv = '''
Manager:

    Screen1:
    Screen2:
    Screen3:
    Screen4:
    Screen5:

<Screen1>:
    name:"first"
    id:screen1
    BoxLayout:
        orientation: 'vertical'
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: 'Select available players'
                # text_size: self.size
                size_hint:(.5, 1)

            Button:
                id:butt
                text:'Create Teams'
                # text_size: self.size
                size_hint:(.5,1)

                on_press:
                    root.calledwithbutton()
                    root.whos_playing=players.whos_playing
                    root.process_stuff()
                    # root.plot_graph()
                    # root.manager.screens[1].ids.imageView.source = 'graph.png'
                    root.manager.screens[1].ids.my_Label1_1.text = root.team1_txt
                    root.manager.screens[1].ids.my_Label2_1.text = root.team2_txt
                    root.manager.screens[1].ids.my_Label1.text = root.cap1
                    root.manager.screens[1].ids.my_Label2.text = root.cap2
                    root.manager.screens[1].ids.my_Label2_3.text = root.avg_2
                    root.manager.screens[1].ids.my_Label1_3.text = root.avg_1
                    root.manager.screens[1].ids.my_Label_head.text = root.rec_overs
                    root.manager.screens[1].ids.my_Label1_4.text = root.team1_runs_bowl
                    root.manager.screens[1].ids.my_Label2_4.text = root.team2_runs_bowl




        MultiSelectSpinners:
            id:players
            values:root.drop_values
            size_hint:(1, 1)
<Screen2>:
    name:"second"

    BoxLayout:


        orientation:'vertical'
        BoxLayout:

            orientation:'vertical'
            Label:
                # halign: "center"
                valign: "top"
                id:my_Label_head
                size:self.size
                font_size:30
                text_size: self.size
                text:
                    root.rec_overs
            Label:
                id:my_Label1
                valign: "top"
                size:self.size
                font_size:35
                text_size: self.size
                text:
                    root.cap1
            Label:
                # halign: "center"
                valign: "top"
                id:my_Label1_3
                size:self.size
                font_size:30
                text_size: self.size
                text:
                    root.avg_1
            Label:
                id:my_Label1_4
                valign: "top"
                size:self.size
                text_size: self.size
                font_size:30
                text:
                    root.team1_runs_bowl
            Label:
                id:my_Label1_1
                valign: "top"
                size:self.size
                text_size: self.size
                font_size:25
                text:
                    root.team1_txt

        BoxLayout:

            orientation:'vertical'
            Label:
                # halign: "center"
                valign: "top"
                id:my_Label2
                size:self.size
                font_size:35
                text_size: self.size
                text:
                    root.cap2
            Label:
                # halign: "center"
                valign: "top"
                id:my_Label2_3
                size:self.size
                font_size:30
                text_size: self.size
                text:
                    root.avg_2
            Label:
                id:my_Label2_4
                valign: "top"
                size:self.size
                text_size: self.size
                font_size:30
                text:
                    root.team2_runs_bowl
            Label:
                id:my_Label2_1
                valign: "top"
                size:self.size
                text_size: self.size
                font_size:25
                text:
                    root.team1_txt


    BoxLayout:
        orientation:'horizontal'
        Button:
            text:'Create again'
            size_hint:(1,.05)
            font_size:30
            on_press:
                root.calledwithbutton()
                # imageView.source=''
        Button:
            text:'Call for Toss?'
            size_hint:(1,.05)
            font_size:30
            on_press:
                root.calledwithbuttongif()
                root.manager.screens[2].ids.giffy.anim_delay = 0.10
                root.manager.screens[2].ids.giffy._coreimage.anim_reset(True)
<Screen3>:
    name:"gif"
    Image:
        id: giffy
        source: 'toss.gif'
        center: self.parent.center
        size: 500, 500
        allow_stretch: True
        anim_delay: -1
        anim_loop: 1
<Screen4>:
    name:"third"
    Label:
        text:"Head"
    BoxLayout:
        orientation:'horizontal'
        Button:
            text:'Toss Again?'
            size_hint:(1,.05)
            font_size:30
            on_press:
                root.callbackfun()
                root.manager.screens[2].ids.giffy.anim_delay = 0.10
                root.manager.screens[2].ids.giffy._coreimage.anim_reset(True)
        Button:
            text:'Check teams again?'
            size_hint:(1,.05)
            font_size:30
            on_press:
                root.manager.current = "second"
<Screen5>:
    name:"fourth"
    Label:
        text:"Tail"
    BoxLayout:
        orientation:'horizontal'
        Button:
            text:'Toss Again?'
            size_hint:(1,.05)
            font_size:30
            on_press:
                root.callbackfun()
                root.manager.screens[2].ids.giffy.anim_delay = 0.10
                root.manager.screens[2].ids.giffy._coreimage.anim_reset(True)
        Button:
            text:'Check teams again?'
            size_hint:(1,.05)
            font_size:30
            on_press:
                root.manager.current = "second"




<MultiSelectOption@ToggleButton>:
    size_hint: 1, None
    height: '40dp'

'''

if __name__=="__main__":

    runTouchApp(Builder.load_string(kv))

import pyautogui
import time

"""
What is Mike?
-----------------
Mike is a program used to parse through the unformatted total responses of a multi-select question in Microsoft Forms, collect and order the data into a neat list, and then enter the data into an Excel spreadsheet by way of a macro.


How to Use Mike
-----------------
For every new survey question to macro, update these variables:

* all_choices_ordered 
	- a list of the choices on the survey 
	- when creating the survey, choices CANNOT contain commas 
	- ordering of this list must correlate to the actual order of the responses in the survey 

* str_responses 	
	- copy and paste all responses into this string
	- make sure to get the data from all the multiple pages (like if there's 332 responses, only 1-188 are on page 1, don't forget to grab the rest of the responses on the next page)
	- ensure when copying and pasting multiple times, characters (especially these ones: [, ], ") aren't removed

"""

# ----- update me! ------

all_choices_ordered = [

"A place for useful info/updates",
"Chill worktime",
"Teacher help time",
"Clutch worktime",
"Relaxing",
"Snack time",
"Nap time",
"A place to socialize",
"Awkward",
"A waste of time",
"A skippable period"

]

"""
----------------------------------------
Text Parsing Functions
----------------------------------------
"""

# represents a single response, where the responses of the individual are stored in a list (ex: ["Y", Y", "N"]) called self.activities
class IndividualResponse:
	def __init__(self, response):

		self.activities = []
		self.init_activities()
		self.response_to_YN(response)

	# intializes the activities list to be the same size as the all_choices_ordered and fills it with "N"
	def init_activities(self):

		for n in range(len(all_choices_ordered)):

			self.activities.append("N")

	# updates the entry of self.activities to "Y" at the location that corresponds to the location where a given choice is located in all_choices_ordered
	def update_activities(self, response):

		for n in range(len(all_choices_ordered)):

			if (response == all_choices_ordered[n]):
				self.activities[n] = "Y"
				continue

	# takes in an individual response list, checks which choices are included, and updates the activities accordingly
	def response_to_YN(self, response):

		for a in all_choices_ordered:

			for r in response:

				if (a == r):
					self.update_activities(a)

	# when this the IndividualResponse object is printed, instead of returning a string of the object's location memory, it returns self.activities as a string
	def __str__(self):
		return str(self.activities)

# takes in the entire unformatted responses from Microsoft Forms as a chunky string and parses it to get individuals' responses, returns a list of the lists of strings of the parts of individuals' responses
def parse(input):

	# all indi_responses is a list of individual responses
	all_indi_responses = []

	# curr_indi_response is a list of the current parts of the individual response 
	curr_indi_response = []

	# curr_string is the curr part of the individual response
	curr_string = ""

	for i in range(len(input)):
		
		curr_char = input[i]

		# if it finds a ([), a new individual response has occurred and curr_indi_response, curr_string are reset
		if (curr_char == "["):

			curr_indi_response = []
			curr_string = ""

		# if it finds a ("), the character won't be added
		elif (curr_char == "\""):

			continue

		# if it finds a (,), a distinct part of the response has finished, so it's added to curr_indi_response and curr_string is reset
		elif (curr_char == ","):

			curr_indi_response.append(curr_string)
			curr_string = ""

		# if it finds a (]), a distinct individual response has finished, so it's added to all_indi_responses
		elif (curr_char == "]"):

			# final part of response of an individual doesn't have a comma to mark it, so it has to be manually added here 
			curr_indi_response.append(curr_string)
			curr_string = ""
			all_indi_responses.append(curr_indi_response)
			
		else:
			curr_string += str(curr_char)

	return all_indi_responses

# takes in the list of the lists of strings of the parts of individuals' responses, the list of strings of the parts of individual's response are wrapped into an object, IndividiualResponse, returns a list of IndividualResponse 
def wrap_all_indi_responses_to_object(all_indi_responses):

	all_indi_responses_wrapped = []

	for i in all_indi_responses:

		converted = IndividualResponse(i)
		all_indi_responses_wrapped.append(converted)

	return all_indi_responses_wrapped


"""
----------------------------------------
Quality Assurance Functions
----------------------------------------
"""

# print the total number of responses and frequency of responses
def check_stats(all_indi_responses):

	total_num_responses = len(all_indi_responses)

	print("\nStatistics:")
	print(str(total_num_responses) + " total responses.")

	for choice in all_choices_ordered:

		counter = 0

		for indi_response in all_indi_responses:

			for x in indi_response:

				if x == choice:

					counter += 1

		print("\"" + choice + "\" - " + str(counter) + " respondents")
	print("")

# prints the contents of a particular individual response based on its RESPONSE NUMBER, NOT list index
def index_response(index, all_indi_responses, wrapped=False):

	# to reiterate, inputted index is NOT based on traditional indices of lists/coding
	index -= 1

	# wrapped=True AND inputted list must be a list of IndividualResponse objects
	if (wrapped):

		print(all_indi_responses[index].activities)

	# wrapped=False AND inputted list is a list of lists of parts of responses
	else:

		print(all_indi_responses[index])


"""
----------------------------------------
Macro Functions
----------------------------------------
"""

# a macro that enters the Y and N data into excel with pyautogui
def macro(all_indi_responses_wrapped):

	print("Hi! My name is Mike the Macro! ")

	start = input("Enter anything, and then I'll start a 10 second timer before I get the ball rolling. ")
	
	time.sleep(10)
	
	for x in all_indi_responses_wrapped:

		# writing a row entry for an individual response
		for g in x.activities:

			pyautogui.write(g, interval=0.01)
			time.sleep(0.1)
			pyautogui.press("right")
			time.sleep(0.1)

		# moving the cursor one cell down and to the left back to the initial row position
		pyautogui.press("down")

		for n in range(len(x.activities)):

			pyautogui.press("left")
			time.sleep(0.01)

		time.sleep(0.1)

# ----- update me! ------

str_responses = """

1	anonymous	["A skippable period","A place for useful info/updates","Clutch worktime"]
2	anonymous	["Chill worktime","Snack time","A place to socialize"]
3	anonymous	["Snack time","Nap time","A place to socialize"]
4	anonymous	["Chill worktime","A place to socialize"]
5	anonymous	["A skippable period","Nap time","Snack time","Relaxing","Clutch worktime"]
6	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize"]
7	anonymous	["A place to socialize","Relaxing","Chill worktime","Teacher help time"]
8	anonymous	["Chill worktime","Clutch worktime","Relaxing"]
9	anonymous	["A place for useful info/updates"]
10	anonymous	["Nap time","A place to socialize","A skippable period"]
11	anonymous	["Nap time","Awkward"]
12	anonymous	["Chill worktime","A waste of time","A skippable period"]
13	anonymous	["A place for useful info/updates","Chill worktime","Relaxing","Snack time","A place to socialize"]
14	anonymous	["Clutch worktime","Chill worktime","Snack time"]
15	anonymous	["Chill worktime","Relaxing"]
16	anonymous	["Relaxing","A place to socialize","Chill worktime"]
17	anonymous	["Clutch worktime","Chill worktime","Relaxing","Snack time","Nap time","A place to socialize","A skippable period"]
18	anonymous	["Clutch worktime","Relaxing","Snack time"]
19	anonymous	["A place to socialize"]
20	anonymous	["A waste of time","A skippable period"]
21	anonymous	["A waste of time","Clutch worktime","A skippable period"]
22	anonymous	["A waste of time","Clutch worktime","A place to socialize"]
23	anonymous	["Chill worktime","Relaxing","Snack time","Nap time","A place to socialize","A skippable period"]
24	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize","Awkward","A waste of time","A skippable period"]
25	anonymous	["Relaxing","Snack time","Nap time","A place to socialize","A waste of time","A skippable period"]
26	anonymous	["A place for useful info/updates","Chill worktime","A place to socialize","Clutch worktime"]
27	anonymous	["Chill worktime","Clutch worktime","Relaxing","Snack time","A place to socialize","A place for useful info/updates"]
28	anonymous	["Chill worktime","Clutch worktime","Relaxing","Nap time"]
29	anonymous	["Nap time","Awkward","Chill worktime"]
30	anonymous	["Awkward","A waste of time","A skippable period"]
31	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing","Snack time"]
32	anonymous	["Relaxing"]
33	anonymous	["Relaxing","Chill worktime","A place to socialize"]
34	anonymous	["Chill worktime","Relaxing","Nap time"]
35	anonymous	["Relaxing","Nap time","Awkward","A place for useful info/updates","Chill worktime","Clutch worktime","Snack time"]
36	anonymous	["A waste of time"]
37	anonymous	["Relaxing","Snack time","Nap time","A skippable period"]
38	anonymous	["Chill worktime","Relaxing","Snack time","A waste of time","A skippable period"]
39	anonymous	["Chill worktime","Relaxing","Snack time","Nap time","A place to socialize"]
40	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing","Nap time"]
41	anonymous	["Chill worktime","Relaxing","Awkward"]
42	anonymous	["A skippable period","A waste of time","Snack time","Nap time"]
43	anonymous	["Relaxing","Nap time"]
44	anonymous	["A waste of time","Nap time"]
45	anonymous	["Relaxing","A place for useful info/updates","Clutch worktime"]
46	anonymous	["Nap time","Awkward"]
47	anonymous	["Chill worktime","Awkward","A skippable period","Relaxing"]
48	anonymous	["Chill worktime","Clutch worktime","Relaxing"]
49	anonymous	["Relaxing","Chill worktime","A place to socialize","A waste of time"]
50	anonymous	["Relaxing","Chill worktime"]
51	anonymous	["Clutch worktime","Snack time"]
52	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize"]
53	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize","A place for useful info/updates","Clutch worktime"]
54	anonymous	["Nap time","A skippable period","Chill worktime"]
55	anonymous	["Chill worktime","Nap time"]
56	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","Snack time","A place to socialize"]
57	anonymous	["Snack time","Nap time","Chill worktime"]
58	anonymous	["Chill worktime","Relaxing","Snack time","Nap time","A place to socialize"]
59	anonymous	["Chill worktime","Relaxing","Snack time","Nap time","A place to socialize"]
60	anonymous	["Clutch worktime","A place to socialize"]
61	anonymous	["Relaxing","Snack time","A place to socialize"]
62	anonymous	["Teacher help time","Chill worktime","A place to socialize","A waste of time"]
63	anonymous	["Chill worktime","Clutch worktime","Nap time"]
64	anonymous	["Chill worktime","Snack time","A place to socialize","Awkward"]
65	anonymous	["Chill worktime","Relaxing","Snack time","Nap time","A place to socialize"]
66	anonymous	["Chill worktime","Relaxing","Snack time","A skippable period"]
67	anonymous	["A waste of time"]
68	anonymous	["Clutch worktime"]
69	anonymous	["Chill worktime","A place for useful info/updates","Relaxing"]
70	anonymous	["Chill worktime","Relaxing","Snack time","Nap time"]
71	anonymous	["Snack time","Awkward","A waste of time","A skippable period"]
72	anonymous	["Relaxing","A place to socialize","Chill worktime"]
73	anonymous	["Chill worktime"]
74	anonymous	["A waste of time","Awkward","Chill worktime"]
75	anonymous	["Awkward","A skippable period"]
76	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing"]
77	anonymous	["Snack time","A place to socialize"]
78	anonymous	["Chill worktime","Clutch worktime","Relaxing","A place to socialize"]
79	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","A place to socialize"]
80	anonymous	["A place to socialize","A skippable period","Chill worktime"]
81	anonymous	["Chill worktime","Teacher help time","Relaxing","Snack time","A place to socialize"]
82	anonymous	["Chill worktime","A place to socialize","A skippable period","Clutch worktime"]
83	anonymous	["Chill worktime","Clutch worktime","Relaxing","Snack time","Awkward","A waste of time"]
84	anonymous	["Chill worktime","Clutch worktime","A skippable period","A place to socialize"]
85	anonymous	["A place to socialize","Chill worktime","Relaxing"]
86	anonymous	["Clutch worktime","Relaxing","A waste of time","A skippable period"]
87	anonymous	["Chill worktime","Teacher help time","Relaxing","Nap time"]
88	anonymous	["Chill worktime","A waste of time","A skippable period"]
89	anonymous	["Chill worktime","Snack time"]
90	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize"]
91	anonymous	["Chill worktime","Clutch worktime","Relaxing","A place to socialize","A place for useful info/updates"]
92	anonymous	["Chill worktime","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize","A skippable period"]
93	anonymous	["Chill worktime","Snack time","Relaxing","A place to socialize","Teacher help time"]
94	anonymous	["Clutch worktime"]
95	anonymous	["A waste of time","A place to socialize","Clutch worktime","Snack time","Relaxing","Awkward"]
96	anonymous	["Clutch worktime","Snack time","A place for useful info/updates"]
97	anonymous	["Nap time","Chill worktime","Clutch worktime","Snack time","Relaxing","A place to socialize"]
98	anonymous	["Chill worktime","Teacher help time","Clutch worktime","Nap time"]
99	anonymous	["A waste of time","A skippable period","Awkward","A place to socialize","Nap time","Snack time","Relaxing","Clutch worktime","Chill worktime","A place for useful info/updates","Teacher help time"]
100	anonymous	["Relaxing","A place to socialize","Chill worktime"]
101	anonymous	["Relaxing","A place to socialize"]
102	anonymous	["Chill worktime","Relaxing","Snack time"]
103	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","Snack time","Awkward"]
104	anonymous	["A waste of time","A skippable period","Nap time"]
105	anonymous	["Relaxing","Nap time","Clutch worktime"]
106	anonymous	["Chill worktime","A place for useful info/updates","Clutch worktime","Nap time"]
107	anonymous	["Relaxing","Chill worktime","A place to socialize","Teacher help time"]
108	anonymous	["Chill worktime","Relaxing","A place to socialize","A waste of time"]
109	anonymous	["Chill worktime","Snack time","A place for useful info/updates","Relaxing"]
110	anonymous	["A waste of time","A skippable period"]
111	anonymous	["Snack time","Nap time","A place to socialize","Chill worktime"]
112	anonymous	["A skippable period","A waste of time","Awkward","A place to socialize","Nap time","Snack time","Relaxing","Clutch worktime","Teacher help time","Chill worktime","A place for useful info/updates"]
113	anonymous	["Chill worktime","Relaxing","Snack time","Nap time"]
114	anonymous	["Nap time","A place to socialize","Snack time","Relaxing","Clutch worktime","Chill worktime","Teacher help time"]
115	anonymous	["Snack time","Nap time"]
116	anonymous	["Chill worktime","Clutch worktime"]
117	anonymous	["Snack time","Chill worktime","A place to socialize"]
118	anonymous	["Nap time","Snack time","Relaxing","Chill worktime","A place to socialize"]
119	anonymous	["Clutch worktime"]
120	anonymous	["A place to socialize","Nap time","Relaxing","Clutch worktime"]
121	anonymous	["Relaxing","A waste of time","Snack time"]
122	anonymous	["Chill worktime","Nap time","Awkward","A waste of time","A skippable period","A place to socialize","Snack time","Relaxing","Clutch worktime","Teacher help time","A place for useful info/updates"]
123	anonymous	["Nap time","A waste of time"]
124	anonymous	["Clutch worktime","Chill worktime","Snack time","Nap time"]
125	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing","Snack time","A place to socialize"]
126	anonymous	["Chill worktime"]
127	anonymous	["Relaxing","Snack time","Chill worktime"]
128	anonymous	["Snack time","Clutch worktime","Relaxing","Chill worktime"]
129	anonymous	["Awkward","A waste of time","A skippable period"]
130	anonymous	["Nap time","Awkward"]
131	anonymous	["Nap time"]
132	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize","A place for useful info/updates"]
133	anonymous	["A place to socialize"]
134	anonymous	["Chill worktime","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize"]
135	anonymous	["Relaxing","Clutch worktime","A place to socialize"]
136	anonymous	["Chill worktime"]
137	anonymous	["A waste of time"]
138	anonymous	["Chill worktime","Clutch worktime","A skippable period"]
139	anonymous	["Relaxing","Clutch worktime","Chill worktime"]
140	anonymous	["Clutch worktime"]
141	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize","Awkward","A waste of time","A skippable period"]
142	anonymous	["Awkward","A place to socialize"]
143	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize"]
144	anonymous	["Chill worktime","Awkward","A skippable period"]
145	anonymous	["Chill worktime","Snack time"]
146	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","Snack time","Awkward"]
147	anonymous	["Chill worktime"]
148	anonymous	["Snack time","Nap time","A place to socialize","Relaxing","Clutch worktime","Chill worktime"]
149	anonymous	["Chill worktime","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize","A place for useful info/updates"]
150	anonymous	["Chill worktime","Relaxing","Snack time","A waste of time","A place to socialize"]
151	anonymous	["A skippable period"]
152	anonymous	["Chill worktime","Clutch worktime","Relaxing","A place to socialize","A place for useful info/updates"]
153	anonymous	["Chill worktime","Clutch worktime","Relaxing","Nap time","A place to socialize","A waste of time","A skippable period","Awkward"]
154	anonymous	["Chill worktime","Relaxing","Nap time"]
155	anonymous	["Clutch worktime","Chill worktime","A place to socialize","Nap time","Relaxing"]
156	anonymous	["Chill worktime","Awkward","Relaxing"]
157	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Snack time","A place to socialize"]
158	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize"]
159	anonymous	["Chill worktime","Teacher help time"]
160	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize"]
161	anonymous	["Relaxing","Snack time","Nap time","A place to socialize","A waste of time","A skippable period"]
162	anonymous	["Clutch worktime","Awkward","A place to socialize","A waste of time","Snack time","Chill worktime","A place for useful info/updates"]
163	anonymous	["Clutch worktime"]
164	anonymous	["A place for useful info/updates","Clutch worktime","Snack time"]
165	anonymous	["Chill worktime","Relaxing","A waste of time"]
166	anonymous	["Relaxing"]
167	anonymous	["Chill worktime","Clutch worktime","Relaxing","Nap time","Snack time","A place to socialize","A skippable period"]
168	anonymous	["A place for useful info/updates","Snack time","Clutch worktime"]
169	anonymous	["Relaxing","Chill worktime"]
170	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","Nap time","A place to socialize"]
171	anonymous	["Chill worktime","Teacher help time","Clutch worktime","Snack time","A place for useful info/updates","Relaxing"]
172	anonymous	["A waste of time","A skippable period","Snack time"]
173	anonymous	["Chill worktime","A place to socialize","Snack time"]
174	anonymous	["A waste of time"]
175	anonymous	["Chill worktime","Relaxing","Nap time","A place to socialize"]
176	anonymous	["Chill worktime","Relaxing","Snack time","Nap time"]
177	anonymous	["Chill worktime","Teacher help time","Snack time"]
178	anonymous	["A waste of time","A skippable period","A place to socialize"]
179	anonymous	["Chill worktime","Awkward","A waste of time","A place to socialize","A skippable period","Snack time","Nap time"]
180	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Relaxing","Snack time","Nap time","A skippable period","A waste of time"]
181	anonymous	["Snack time","Awkward","A skippable period"]
182	anonymous	["Chill worktime","Clutch worktime"]
183	anonymous	["Nap time"]
184	anonymous	["A place for useful info/updates","Chill worktime","Relaxing","Teacher help time"]
185	anonymous	["A waste of time","Awkward"]
186	anonymous	["Chill worktime","A place for useful info/updates","Relaxing","Nap time","A place to socialize"]
187	anonymous	["Chill worktime","Snack time","A skippable period"]
188	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Relaxing","Snack time","Nap time","A place to socialize","Clutch worktime"]
189	anonymous	["Chill worktime"]
190	anonymous	["A waste of time","A place to socialize","Relaxing","Clutch worktime"]
191	anonymous	["Nap time"]
192	anonymous	["Chill worktime","Snack time","Relaxing","A place to socialize"]
193	anonymous	["Nap time"]
194	anonymous	["Awkward","Chill worktime","Snack time"]
195	anonymous	["Chill worktime","Clutch worktime","A waste of time","A skippable period","Awkward","A place to socialize","Nap time","Snack time","Relaxing","Teacher help time"]
196	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize","A skippable period","A waste of time"]
197	anonymous	["Relaxing","Snack time","A place to socialize","Chill worktime"]
198	anonymous	["Clutch worktime","Snack time","Nap time"]
199	anonymous	["A place for useful info/updates","Chill worktime","Relaxing","Snack time"]
200	anonymous	["Nap time"]
201	anonymous	["A place to socialize","Relaxing"]
202	anonymous	["Clutch worktime","Snack time","A place to socialize"]
203	anonymous	["Chill worktime","A place to socialize","A skippable period"]
204	anonymous	["Chill worktime","Relaxing","Nap time","Awkward","A waste of time"]
205	anonymous	["Nap time","Chill worktime","Clutch worktime"]
206	anonymous	["Clutch worktime","Chill worktime","Snack time","Nap time","A skippable period"]
207	anonymous	["Chill worktime","Teacher help time","Clutch worktime"]
208	anonymous	["Teacher help time","Clutch worktime","Relaxing","Snack time","A place to socialize"]
209	anonymous	["Relaxing","Snack time","A place to socialize","Chill worktime","Clutch worktime"]
210	anonymous	["Chill worktime"]
211	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Relaxing","Snack time"]
212	anonymous	["Chill worktime","Clutch worktime","Nap time","A waste of time"]
213	anonymous	["Chill worktime","Snack time","Awkward","A waste of time","A skippable period"]
214	anonymous	["Nap time","Snack time","A skippable period","A waste of time"]
215	anonymous	["Chill worktime","Nap time","A skippable period","A waste of time"]
216	anonymous	["Chill worktime","Teacher help time","A place for useful info/updates","Clutch worktime","Relaxing","Nap time","Snack time","A place to socialize"]
217	anonymous	["A place for useful info/updates","Chill worktime","Relaxing","Snack time","Nap time"]
218	anonymous	["Chill worktime"]
219	anonymous	["Clutch worktime","Nap time","Relaxing","A place for useful info/updates"]
220	anonymous	["Chill worktime","Clutch worktime","Snack time","Relaxing","A place to socialize"]
221	anonymous	["Chill worktime","Clutch worktime","Relaxing","A place to socialize"]
222	anonymous	["Chill worktime","A place for useful info/updates","Clutch worktime","Relaxing","Nap time","Awkward"]
223	anonymous	["Chill worktime","Relaxing","Snack time","Nap time","A place to socialize"]
224	anonymous	["A place for useful info/updates","Chill worktime","Relaxing"]
225	anonymous	["A place to socialize","Nap time","Relaxing","Clutch worktime"]
226	anonymous	["Chill worktime","Clutch worktime","Relaxing","A place to socialize","Snack time","Nap time"]
227	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","Nap time","Awkward"]
228	anonymous	["Relaxing","Nap time"]
229	anonymous	["Clutch worktime","Snack time","A place to socialize","A waste of time"]
230	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize"]
231	anonymous	["Chill worktime","Relaxing","A place to socialize"]
232	anonymous	["A skippable period"]
233	anonymous	["A waste of time","Relaxing","A place to socialize"]
234	anonymous	["Chill worktime","Nap time","Snack time"]
235	anonymous	["Chill worktime","Clutch worktime","Relaxing","A place to socialize"]
236	anonymous	["Chill worktime","Clutch worktime","A place to socialize"]
237	anonymous	["Chill worktime","A place to socialize"]
238	anonymous	["Chill worktime","Clutch worktime","Relaxing","Snack time","A place to socialize"]
239	anonymous	["Chill worktime","Relaxing"]
240	anonymous	["Nap time","A place to socialize","Awkward","A waste of time","A skippable period","Snack time"]
241	anonymous	["Clutch worktime","Nap time","Relaxing"]
242	anonymous	["Nap time","Clutch worktime","Teacher help time"]
243	anonymous	["A place for useful info/updates","Chill worktime","Relaxing"]
244	anonymous	["Chill worktime","Relaxing","Snack time","Nap time","A place to socialize","Awkward","A skippable period"]
245	anonymous	["Clutch worktime","Relaxing","Snack time","Awkward","A waste of time"]
246	anonymous	["Chill worktime","Clutch worktime","Relaxing","A place to socialize"]
247	anonymous	["A place for useful info/updates","Chill worktime","Relaxing"]
248	anonymous	["Chill worktime","Clutch worktime","Relaxing","Snack time","A place to socialize"]
249	anonymous	["Snack time","A waste of time","A skippable period"]
250	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize","Clutch worktime"]
251	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","A place to socialize"]
252	anonymous	["A place to socialize","Snack time","Chill worktime"]
253	anonymous	["Chill worktime","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize"]
254	anonymous	["Chill worktime","Clutch worktime","Relaxing","Nap time"]
255	anonymous	["Chill worktime","Awkward","A waste of time","A place to socialize","Nap time","Snack time"]
256	anonymous	["A place to socialize","A skippable period","Snack time"]
257	anonymous	["Chill worktime","Clutch worktime","Nap time","A place for useful info/updates"]
258	anonymous	["Chill worktime","Snack time","Relaxing","A place to socialize","Clutch worktime"]
259	anonymous	["Nap time"]
260	anonymous	["Chill worktime","Relaxing","Snack time"]
261	anonymous	["Chill worktime","Clutch worktime","A place to socialize"]
262	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize","Awkward","A waste of time","A skippable period","Teacher help time"]
263	anonymous	["Clutch worktime"]
264	anonymous	["Teacher help time","Chill worktime"]
265	anonymous	["Chill worktime","Nap time","A place to socialize"]
266	anonymous	["Chill worktime","Relaxing","A place to socialize","Awkward","A waste of time"]
267	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize"]
268	anonymous	["Chill worktime","Nap time","Snack time","A waste of time","Relaxing","A skippable period","Clutch worktime","Teacher help time","A place to socialize"]
269	anonymous	["Nap time","Relaxing"]
270	anonymous	["Chill worktime","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize"]
271	anonymous	["Clutch worktime","Relaxing","Snack time","Nap time"]
272	anonymous	["Chill worktime","A place for useful info/updates","Relaxing","Clutch worktime"]
273	anonymous	["Chill worktime","A place to socialize","A waste of time","Snack time","Teacher help time"]
274	anonymous	["Chill worktime","Relaxing","Clutch worktime"]
275	anonymous	["A place for useful info/updates","Chill worktime","Snack time","Nap time","Relaxing"]
276	anonymous	["A place for useful info/updates","Relaxing","Chill worktime"]
277	anonymous	["Clutch worktime","Chill worktime","Snack time","Relaxing"]
278	anonymous	["Clutch worktime","Snack time","A place to socialize","Chill worktime","Relaxing"]
279	anonymous	["Clutch worktime","A place to socialize"]
280	anonymous	["Chill worktime"]
281	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize"]
282	anonymous	["Chill worktime","Relaxing","Nap time"]
283	anonymous	["Chill worktime","Relaxing"]
284	anonymous	["Teacher help time","Chill worktime","A place for useful info/updates","Clutch worktime","Snack time"]
285	anonymous	["Snack time","Nap time","A waste of time","A skippable period","Clutch worktime","Chill worktime","Relaxing"]
286	anonymous	["Chill worktime","A waste of time"]
287	anonymous	["Chill worktime","Relaxing","Teacher help time","Clutch worktime"]
288	anonymous	["Chill worktime","Clutch worktime","Snack time"]
289	anonymous	["Chill worktime","A place to socialize","Clutch worktime"]
290	anonymous	["Chill worktime","A place for useful info/updates","Teacher help time","Snack time","Nap time"]
291	anonymous	["Relaxing","Snack time","A place to socialize"]
292	anonymous	["Chill worktime","Relaxing"]
293	anonymous	["Chill worktime","Clutch worktime","Nap time","A place to socialize"]
294	anonymous	["Chill worktime","A place to socialize","Snack time","Relaxing","Clutch worktime"]
295	anonymous	["Chill worktime","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize"]
296	anonymous	["Teacher help time","Chill worktime","Relaxing","Snack time"]
297	anonymous	["Chill worktime","Clutch worktime","A place to socialize","Relaxing"]
298	anonymous	["A waste of time"]
299	anonymous	["Chill worktime","A place for useful info/updates","Clutch worktime","Relaxing","Snack time","Nap time","A skippable period"]
300	anonymous	["Nap time","A place to socialize","Chill worktime"]
301	anonymous	["Clutch worktime","Chill worktime","Relaxing"]
302	anonymous	["Nap time","Snack time","Relaxing","Clutch worktime"]
303	anonymous	["Chill worktime"]
304	anonymous	["Chill worktime","A place for useful info/updates","Clutch worktime","Relaxing","Snack time","A place to socialize"]
305	anonymous	["Chill worktime"]
306	anonymous	["A place for useful info/updates","Chill worktime","Relaxing","Snack time","Awkward","A waste of time"]
307	anonymous	["Clutch worktime","Relaxing","A place to socialize","A place for useful info/updates","Chill worktime","Teacher help time","Snack time","Nap time"]
308	anonymous	["Chill worktime"]
309	anonymous	["Chill worktime","Clutch worktime","Snack time","Relaxing"]
310	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing","A place to socialize"]
311	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Snack time","Relaxing","A place to socialize"]
312	anonymous	["Chill worktime","A place to socialize"]
313	anonymous	["Chill worktime","Teacher help time","Clutch worktime","Relaxing"]
314	anonymous	["A waste of time","A skippable period","A place for useful info/updates"]
315	anonymous	["A skippable period","Chill worktime"]
316	anonymous	["Nap time"]
317	anonymous	["Chill worktime","Snack time"]
318	anonymous	["A waste of time"]
319	anonymous	["Chill worktime","Snack time","Relaxing","Clutch worktime","A place for useful info/updates","A place to socialize"]
320	anonymous	["Clutch worktime","Nap time","A place to socialize"]
321	anonymous	["Chill worktime","Clutch worktime","Snack time"]
322	anonymous	["A place to socialize","Snack time","Nap time","Relaxing"]
323	anonymous	["Nap time","Snack time","Relaxing","Chill worktime"]
324	anonymous	["Relaxing","Snack time","A place to socialize"]
325	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize","Awkward","A waste of time"]
326	anonymous	["A place for useful info/updates","Chill worktime","Relaxing","Snack time"]
327	anonymous	["Snack time","Chill worktime","Relaxing"]
328	anonymous	["Relaxing","Nap time","Snack time"]
329	anonymous	["Nap time","A place to socialize","Snack time","Relaxing","Clutch worktime","Chill worktime","Teacher help time"]
330	anonymous	["A skippable period","A waste of time","Clutch worktime"]
331	anonymous	["Relaxing","Awkward","Chill worktime"]
332	anonymous	["Chill worktime","Teacher help time","Clutch worktime","Relaxing","A place to socialize"]
333	anonymous	["A place to socialize","Relaxing","Chill worktime","Teacher help time"]
334	anonymous	["Chill worktime"]
335	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing","Snack time","A place to socialize"]
336	anonymous	["A place for useful info/updates","Clutch worktime"]
337	anonymous	["Relaxing","A place to socialize","Snack time","Nap time"]
338	anonymous	["A place to socialize","A waste of time","Nap time","Snack time","Clutch worktime"]
339	anonymous	["Chill worktime","Clutch worktime","Relaxing"]
340	anonymous	["Snack time","Teacher help time","Chill worktime","A place for useful info/updates","Relaxing"]
341	anonymous	["Chill worktime","Relaxing","Snack time","Nap time"]
342	anonymous	["Chill worktime","Clutch worktime","Relaxing"]
343	anonymous	["Nap time","Snack time","Clutch worktime"]
344	anonymous	["Clutch worktime","Relaxing","Snack time","Nap time","Awkward","A waste of time","A skippable period"]
345	anonymous	["Chill worktime","Relaxing","Snack time"]
346	anonymous	["Chill worktime","Clutch worktime","Relaxing","A place to socialize"]
347	anonymous	["Chill worktime","Clutch worktime","A skippable period"]
348	anonymous	["Snack time"]
349	anonymous	["Nap time"]
350	anonymous	["Chill worktime","Clutch worktime","A place to socialize","Snack time"]
351	anonymous	["Clutch worktime","Relaxing","A place to socialize"]
352	anonymous	["Awkward","Clutch worktime"]
353	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize","A skippable period"]
354	anonymous	["Clutch worktime","Nap time","A place to socialize"]
355	anonymous	["A place to socialize","Snack time","Clutch worktime"]
356	anonymous	["Chill worktime"]
357	anonymous	["Relaxing","Awkward","A skippable period"]
358	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Teacher help time","Relaxing","A place to socialize"]
359	anonymous	["Chill worktime","Relaxing","Snack time","Nap time"]
360	anonymous	["A place to socialize"]
361	anonymous	["Relaxing","Chill worktime"]
362	anonymous	["Chill worktime","Relaxing","Snack time","Nap time"]
363	anonymous	["Chill worktime","Relaxing"]
364	anonymous	["Relaxing","Snack time","Nap time","A skippable period"]
365	anonymous	["A place to socialize","Relaxing","Chill worktime"]
366	anonymous	["Awkward","A waste of time","A skippable period","Nap time","Snack time"]
367	anonymous	["Snack time","Nap time","A place to socialize","Clutch worktime"]
368	anonymous	["Chill worktime","Clutch worktime","Relaxing","Nap time","A place to socialize"]
369	anonymous	["Chill worktime","Teacher help time","A place to socialize"]
370	anonymous	["Chill worktime","Relaxing","Snack time","Nap time","A place to socialize","A place for useful info/updates","Clutch worktime"]
371	anonymous	["Chill worktime","A place to socialize","Clutch worktime"]
372	anonymous	["Chill worktime","Relaxing","Awkward"]
373	anonymous	["Chill worktime","Relaxing","Snack time","Nap time","A place to socialize"]
374	anonymous	["A waste of time","A skippable period"]
375	anonymous	["A skippable period"]
376	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Relaxing","Snack time","Nap time"]
377	anonymous	["Relaxing"]
378	anonymous	["Relaxing","Snack time","Clutch worktime"]
379	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize"]
380	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize"]
381	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize"]
382	anonymous	["Relaxing","Snack time","Nap time","A place to socialize","Awkward","A waste of time","A skippable period"]
383	anonymous	["Awkward","A waste of time","Chill worktime"]
384	anonymous	["Relaxing"]
385	anonymous	["Chill worktime"]
386	anonymous	["Clutch worktime","Relaxing"]
387	anonymous	["A place to socialize","Clutch worktime"]
388	anonymous	["Chill worktime","Clutch worktime","Relaxing","A waste of time","A skippable period"]
389	anonymous	["Snack time","A place to socialize","Chill worktime","Clutch worktime","A place for useful info/updates"]
390	anonymous	["Snack time","Relaxing"]
391	anonymous	["Chill worktime","Nap time","A place to socialize"]
392	anonymous	["Relaxing","Snack time","Chill worktime"]
393	anonymous	["Relaxing","Snack time","Nap time"]
394	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing","Snack time","A place to socialize"]
395	anonymous	["Chill worktime","Nap time"]
396	anonymous	["Chill worktime","Clutch worktime","Relaxing","A place to socialize"]
397	anonymous	["A place to socialize","Clutch worktime","Chill worktime"]
398	anonymous	["Chill worktime"]
399	anonymous	["Chill worktime","Clutch worktime","Nap time","Relaxing"]
400	anonymous	["Chill worktime","A place for useful info/updates","A skippable period"]
401	anonymous	["Nap time","A place to socialize"]
402	anonymous	["Snack time","Chill worktime","Relaxing"]
403	anonymous	["A waste of time"]
404	anonymous	["Relaxing"]
405	anonymous	["Clutch worktime","Chill worktime","Teacher help time","Relaxing"]
406	anonymous	["Clutch worktime","Relaxing","Snack time"]
407	anonymous	["A waste of time","Awkward","A skippable period"]
408	anonymous	["Chill worktime","Snack time","Relaxing","Clutch worktime"]
409	anonymous	["Relaxing","Chill worktime","Clutch worktime","Snack time"]
410	anonymous	["Clutch worktime","Nap time"]
411	anonymous	["Clutch worktime","A waste of time","A skippable period"]
412	anonymous	["Clutch worktime","Snack time","Chill worktime","Relaxing"]
413	anonymous	["Chill worktime"]
414	anonymous	["A skippable period","A waste of time","A place to socialize","Nap time"]
415	anonymous	["Chill worktime","Nap time","A place to socialize"]
416	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize","Clutch worktime"]
417	anonymous	["Chill worktime","Teacher help time","Relaxing"]
418	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize"]
419	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize"]
420	anonymous	["Relaxing","Snack time","A skippable period","Chill worktime"]
421	anonymous	["Chill worktime"]
422	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","Snack time","Nap time","A place to socialize","Awkward","A waste of time","A skippable period"]
423	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize"]
424	anonymous	["Clutch worktime","Snack time","Chill worktime","A place for useful info/updates"]
425	anonymous	["A skippable period","A place to socialize","Snack time","Relaxing"]
426	anonymous	["A place to socialize","Snack time","Relaxing","Clutch worktime","Teacher help time","Chill worktime","A place for useful info/updates"]
427	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Snack time","Clutch worktime","Nap time","A waste of time","Awkward","A skippable period","A place to socialize","Relaxing"]
428	anonymous	["Clutch worktime","A place to socialize","Nap time","Relaxing"]
429	anonymous	["Clutch worktime","Chill worktime"]
430	anonymous	["A place to socialize","Relaxing","Clutch worktime"]
431	anonymous	["Relaxing","A place to socialize","Chill worktime"]
432	anonymous	["Chill worktime","Clutch worktime","A place for useful info/updates","A place to socialize"]
433	anonymous	["Snack time","A place to socialize","Chill worktime"]
434	anonymous	["A place for useful info/updates","Chill worktime","Snack time","Relaxing","A place to socialize"]
435	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize"]
436	anonymous	["A waste of time","Relaxing","Clutch worktime"]
437	anonymous	["A place to socialize","Relaxing","Teacher help time","Chill worktime"]
438	anonymous	["Snack time","A place for useful info/updates","Clutch worktime","A place to socialize"]
439	anonymous	["A place to socialize","Snack time","Nap time"]
440	anonymous	["Awkward","Clutch worktime","A place for useful info/updates","Snack time"]
441	anonymous	["Chill worktime"]
442	anonymous	["Relaxing","Snack time","Chill worktime"]
443	anonymous	["Relaxing","A skippable period","A place to socialize"]
444	anonymous	["Clutch worktime","Nap time"]
445	anonymous	["A skippable period","Relaxing"]
446	anonymous	["Clutch worktime","A skippable period"]
447	anonymous	["Chill worktime","Relaxing","Snack time","Nap time","A place to socialize"]
448	anonymous	["A place to socialize","Snack time","Relaxing","Chill worktime"]
449	anonymous	["Chill worktime","A place for useful info/updates","Teacher help time","Relaxing"]
450	anonymous	["Chill worktime","Teacher help time","Clutch worktime","Relaxing","Snack time","A place to socialize","A skippable period"]
451	anonymous	["Snack time","A place for useful info/updates","Chill worktime"]
452	anonymous	["Chill worktime","A place for useful info/updates","Teacher help time","Snack time","Relaxing","A place to socialize"]
453	anonymous	["Clutch worktime","Nap time","A place to socialize","A waste of time"]
454	anonymous	["Chill worktime","Clutch worktime","Relaxing"]
455	anonymous	["Chill worktime","Clutch worktime","Snack time"]
456	anonymous	["Chill worktime","Clutch worktime","Relaxing","Snack time","A place to socialize"]
457	anonymous	["Chill worktime","Relaxing","Snack time","Nap time","Clutch worktime","Teacher help time"]
458	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing","A place to socialize"]
459	anonymous	["A place to socialize"]
460	anonymous	["Awkward","A waste of time","A skippable period","Relaxing","Chill worktime"]
461	anonymous	["A place to socialize","Clutch worktime","Teacher help time","Chill worktime","A waste of time","A skippable period"]
462	anonymous	["Clutch worktime","Awkward","Chill worktime"]
463	anonymous	["A place for useful info/updates","Chill worktime","Relaxing","Snack time","A place to socialize","A skippable period"]
464	anonymous	["Chill worktime","A place for useful info/updates","Teacher help time","Snack time","A place to socialize"]
465	anonymous	["Chill worktime","Relaxing","Snack time","Nap time","A place to socialize","Awkward"]
466	anonymous	["Clutch worktime","Snack time","Awkward","A waste of time","A skippable period"]
467	anonymous	["Chill worktime","Clutch worktime","Relaxing"]
468	anonymous	["Chill worktime","Relaxing","Snack time","A place to socialize"]
469	anonymous	["Clutch worktime","Chill worktime","Relaxing","Snack time"]
470	anonymous	["A place for useful info/updates","Clutch worktime","Relaxing","A place to socialize"]
471	anonymous	["Chill worktime","Teacher help time","Clutch worktime","A skippable period"]
472	anonymous	["Chill worktime","Clutch worktime"]
473	anonymous	["Chill worktime"]
474	anonymous	["A place to socialize","Snack time","Nap time","Relaxing"]
475	anonymous	["Chill worktime","Teacher help time","Snack time","Relaxing"]
476	anonymous	["Relaxing","Chill worktime"]
477	anonymous	["A place to socialize","Relaxing","Chill worktime"]
478	anonymous	["A place for useful info/updates","Chill worktime","Relaxing","Awkward"]
479	anonymous	["A place for useful info/updates","Chill worktime","Snack time","Relaxing","A place to socialize","A skippable period"]
480	anonymous	["Chill worktime","A place for useful info/updates","Teacher help time","Clutch worktime"]
481	anonymous	["Chill worktime"]
482	anonymous	["A place to socialize"]
483	anonymous	["A place for useful info/updates","Chill worktime","Relaxing","Snack time","Nap time"]
484	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime","Relaxing","Snack time","Nap time","Awkward"]
485	anonymous	["Chill worktime","Relaxing","Snack time"]
486	anonymous	["Chill worktime","Clutch worktime"]
487	anonymous	["Chill worktime","Clutch worktime","Teacher help time","Relaxing","Nap time","A place to socialize"]
488	anonymous	["Clutch worktime","A place to socialize","Awkward","A place for useful info/updates"]
489	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Clutch worktime"]
490	anonymous	["Nap time","Snack time"]
491	anonymous	["Snack time","Relaxing","Chill worktime"]
492	anonymous	["Clutch worktime"]
493	anonymous	["Chill worktime","Teacher help time","Clutch worktime","A place to socialize"]
494	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime","Relaxing","A place to socialize"]
495	anonymous	["Chill worktime","Clutch worktime","Relaxing","Snack time","A place to socialize"]
496	anonymous	["A place for useful info/updates","Chill worktime","Snack time","A place to socialize"]
497	anonymous	["Chill worktime","Relaxing","Nap time","A place to socialize"]
498	anonymous	["A place for useful info/updates","Chill worktime","Teacher help time","Relaxing","Snack time"]
499	anonymous	["Chill worktime","Teacher help time","Clutch worktime","Snack time","A place to socialize"]
500	anonymous	["A place for useful info/updates","Chill worktime","Clutch worktime"]
501	anonymous	["Clutch worktime","Snack time","Nap time","A place to socialize","A place for useful info/updates","Chill worktime"]
502	anonymous	["Awkward"]
503	anonymous	["A waste of time","A skippable period","A place to socialize"]
504	anonymous	["Chill worktime","Clutch worktime","Snack time","A place to socialize","Awkward","A skippable period","A place for useful info/updates","Teacher help time"]
505	anonymous	["Chill worktime","Snack time","Awkward"]
506	anonymous	["Chill worktime","Teacher help time","Clutch worktime","Snack time","Awkward","A waste of time","A skippable period"]
507	anonymous	["Chill worktime","Clutch worktime","Relaxing","Snack time","A place to socialize"]
508	anonymous	["Chill worktime","Clutch worktime","Relaxing","A place to socialize"]
509	anonymous	["Snack time","A place to socialize","Clutch worktime","Relaxing"]
510	anonymous	["A place for useful info/updates","Chill worktime","Relaxing","Snack time"]
511	anonymous	["Chill worktime","Teacher help time","Clutch worktime","Snack time","A place to socialize"]
512	anonymous	["Relaxing","Snack time"]
513	anonymous	["Relaxing","A place for useful info/updates","Chill worktime"]
514	anonymous	["Relaxing","Nap time"]
515	anonymous	["Clutch worktime","Snack time","A place to socialize","A skippable period","Relaxing","A waste of time"]
516	anonymous	["Clutch worktime","Nap time"]
"""


all_indi_responses = parse(str_responses)
all_indi_responses_wrapped = wrap_all_indi_responses_to_object(all_indi_responses)
check_stats(all_indi_responses)

#index_response(195, all_indi_responses)
#index_response(195, all_indi_responses_wrapped, wrapped=True)

macro(all_indi_responses_wrapped)





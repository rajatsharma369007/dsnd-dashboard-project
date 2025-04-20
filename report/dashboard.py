from fasthtml.common import *
import matplotlib.pyplot as plt

# Import QueryBase, Employee, Team from employee_events
from employee_events import Employee, Team

# import the load_model function from the utils.py file
from utils import load_model

"""
Below, we import the parent classes
you will use for subclassing
"""
from base_components import (
    Dropdown,
    BaseComponent,
    Radio,
    MatplotlibViz,
    DataTable
    )

from combined_components import FormGroup, CombinedComponent


# Create a subclass of base_components/dropdown
# called `ReportDropdown`
class ReportDropdown(Dropdown):
    """
    Class for creating a dropdown component
    for selecting a user type.
    This class provides methods for building
    the dropdown component and retrieving
    the selected user type.
    """
    
    # Overwrite the build_component method
    # ensuring it has the same parameters
    # as the Report parent class's method
    def build_component(self, entity_id, model):
        """
        Build the dropdown component for selecting a user type.
        Args:
            model: The model to use for retrieving user type data.
            **kwargs: Additional keyword arguments.
        """
        #  Set the `label` attribute so it is set
        #  to the `name` attribute for the model
        self.label = model.name
        
        # Return the output from the
        # parent class's build_component method
        return super().build_component(entity_id, model)
    
    # Overwrite the `component_data` method
    # Ensure the method uses the same parameters
    # as the parent class method
    def component_data(self, entity_id, model):
        """
        Get the data for the dropdown component.
        Args:
            model: The model to use for retrieving user type data.
            **kwargs: Additional keyword arguments.
        """
        # Using the model argument
        # call the employee_events method
        # that returns the user-type's
        # names and ids
        return model.names()

# Create a subclass of base_components/BaseComponent
# called `Header`
class Header(BaseComponent):
    """
    Class for creating a header component
    for the report.
    This class provides methods for building
    the header component and retrieving
    the selected user type.
    """

    # Overwrite the `build_component` method
    # Ensure the method has the same parameters
    # as the parent class
    def build_component(self, entity_id, model):
        """
        Build the header component for the report.
        Args:
            model: The model to use for retrieving user type data.
            **kwargs: Additional keyword arguments.
        """
        
        # Using the model argument for this method
        # return a fasthtml H1 objects
        # containing the model's name attribute
        return H1(model.name)
          

# Create a subclass of base_components/MatplotlibViz
# called `LineChart`
class LineChart(MatplotlibViz):
    """
    Class for creating a line chart visualization
    for the report.
    This class provides methods for building
    the line chart visualization and retrieving
    the event counts data.
    """
    
    # Overwrite the parent class's `visualization`
    # method. Use the same parameters as the parent
    def visualization(self, asset_id, model):
        """
        Create a line chart visualization
        for the report.
        Args:
            model: The model to use for retrieving event counts data.
            asset_id: The ID of the asset to visualize.
            **kwargs: Additional keyword arguments.
        """
    

        # Pass the `asset_id` argument to
        # the model's `event_counts` method to
        # receive the x (Day) and y (event count)
        df = model.event_counts(asset_id)
        
        # Use the pandas .fillna method to fill nulls with 0
        df.fillna(0, inplace=True)
        
        # User the pandas .set_index method to set
        # the date column as the index
        df.set_index('event_date', inplace=True)
        
        # Sort the index
        df.sort_index(inplace=True)
        
        # Use the .cumsum method to change the data
        # in the dataframe to cumulative counts
        df = df.cumsum()
        
        
        # Set the dataframe columns to the list
        # ['Positive', 'Negative']
        df.columns = ['Positive', 'Negative']
        
        # Initialize a pandas subplot
        # and assign the figure and axis
        # to variables
        fig, ax = plt.subplots()
        
        # call the .plot method for the
        # cumulative counts dataframe
        df.plot(ax=ax)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        # Use keyword arguments to set 
        # the border color and font color to black. 
        # Reference the base_components/matplotlib_viz file 
        # to inspect the supported keyword arguments
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')
        
        # Set title and labels for x and y axis
        ax.set_title('Cumulative Event Counts', fontsize=20)
        ax.set_xlabel('Date', fontsize=14)
        ax.set_ylabel('Event Count', fontsize=14)


# Create a subclass of base_components/MatplotlibViz
# called `BarChart`
class BarChart(MatplotlibViz):
    """
    Class for creating a bar chart visualization
    for the report.
    This class provides methods for building
    the bar chart visualization and retrieving
    the recruitment risk data.
    """

    # Create a `predictor` class attribute
    # assign the attribute to the output
    # of the `load_model` utils function
    predictor = load_model()

    # Overwrite the parent class `visualization` method
    # Use the same parameters as the parent
    def visualization(self, asset_id, model):
        """
        Create a bar chart visualization
        for the report.
        Args:
            model: The model to use for retrieving recruitment risk data.
            asset_id: The ID of the asset to visualize.
            **kwargs: Additional keyword arguments.
        """

        # Using the model and asset_id arguments
        # pass the `asset_id` to the `.model_data` method
        # to receive the data that can be passed to the machine
        # learning model
        data = model.model_data(asset_id)
        
        # Using the predictor class attribute
        # pass the data to the `predict_proba` method
        prob = self.predictor.predict_proba(data)

        # Index the second column of predict_proba output
        # The shape should be (<number of records>, 1)
        prob = prob[:, 1]
        
        
        # Below, create a `pred` variable set to
        # the number we want to visualize
        #
        # If the model's name attribute is "team"
        # We want to visualize the mean of the predict_proba output
        if model.name == 'team':
            # Set `pred` to the mean of the predict_proba output
            pred = prob.mean()
        # Otherwise set `pred` to the first value
        # of the predict_proba output
        else:
            # Set `pred` to the first value of the predict_proba output
            pred = prob[0]
        
        # Initialize a matplotlib subplot
        fig, ax = plt.subplots()
        
        # Run the following code unchanged
        ax.barh([''], [pred])
        ax.set_xlim(0, 1)
        ax.set_title('Predicted Recruitment Risk', fontsize=20)
        
        # pass the axis variable
        # to the `.set_axis_styling`
        # method
        self.set_axis_styling(ax, bordercolor='black', fontcolor='black')


# Create a subclass of combined_components/CombinedComponent
# called Visualizations       
class Visualizations(CombinedComponent):
    """
    Class for creating a combined component
    for the report visualizations.
    This class provides methods for building
    the visualizations component and retrieving
    the event counts and recruitment risk data.
    """

    # Set the `children`
    # class attribute to a list
    # containing an initialized
    # instance of `LineChart` and `BarChart`
    children = [
        LineChart(),
        BarChart()
    ]

    # Leave this line unchanged
    outer_div_type = Div(cls='grid')
            
# Create a subclass of base_components/DataTable
# called `NotesTable`
class NotesTable(DataTable):
    """
    Class for creating a data table component
    for displaying notes.
    This class provides methods for building
    the notes table component and retrieving
    the notes data.
    """

    # Overwrite the `component_data` method
    # using the same parameters as the parent class
    def component_data(self, entity_id, model):
        """
        Get the data for the notes table component.
        Args:
            model: The model to use for retrieving notes data.
            entity_id: The ID of the entity to retrieve notes for.
            **kwargs: Additional keyword arguments. 
        """
        
        # Using the model and entity_id arguments
        # pass the entity_id to the model's .notes 
        # method. Return the output
        return model.notes(entity_id)
    

class DashboardFilters(FormGroup):

    id = "top-filters"
    action = "/update_data"
    method="POST"

    children = [
        Radio(
            values=["Employee", "Team"],
            name='profile_type',
            hx_get='/update_dropdown',
            hx_target='#selector'
            ),
        ReportDropdown(
            id="selector",
            name="user-selection")
        ]
    
# Create a subclass of CombinedComponents
# called `Report`
class Report(CombinedComponent):
    """
    Class for creating a report component
    for displaying employee and team data.
    This class provides methods for building
    the report component and retrieving
    the selected user type data.
    """

    # Set the `children`
    # class attribute to a list
    # containing initialized instances 
    # of the header, dashboard filters,
    # data visualizations, and notes table
    children = [
        Header(),
        DashboardFilters(),
        Visualizations(),
        NotesTable()
    ]

# Initialize a fasthtml app 
app = FastHTML()

# Initialize the `Report` class
report = Report()


# Create a route for a get request
# Set the route's path to the root
@app.route('/')
def get():
    """
    Render the report component
    Args:
        r: The request object.
    """

    # Call the initialized report
    # pass the integer 1 and an instance
    # of the Employee class as arguments
    # Return the result
    return report("2", Employee())
    

# Create a route for a get request
# Set the route's path to receive a request
# for an employee ID so `/employee/2`
# will return the page for the employee with
# an ID of `2`. 
# parameterize the employee ID 
# to a string datatype
@app.get('/employee/{id: str}')
def employee(id: str):
    """
    Render the report component for an employee.
    Args:
        r: The request object.
        id: The ID of the employee.
    """

    # Call the initialized report
    # pass the ID and an instance
    # of the Employee SQL class as arguments
    # Return the result
    return report(id, Employee())

# Create a route for a get request
# Set the route's path to receive a request
# for a team ID so `/team/2`
# will return the page for the team with
# an ID of `2`. 
# parameterize the team ID 
# to a string datatype
@app.get('/team/{id: str}')
def team(id: str):
    """
    Render the report component for a team.
    Args:
        r: The request object.
        id: The ID of the team.
    """
    # Call the initialized report
    # pass the id and an instance
    # of the Team SQL class as arguments
    # Return the result
    return report(id, Team())


# Keep the below code unchanged!
@app.get('/update_dropdown{r}')
def update_dropdown(r):
    dropdown = DashboardFilters.children[1]
    print('PARAM', r.query_params['profile_type'])
    if r.query_params['profile_type'] == 'Team':
        return dropdown(None, Team())
    elif r.query_params['profile_type'] == 'Employee':
        return dropdown(None, Employee())


@app.post('/update_data')
async def update_data(r):
    from fasthtml.common import RedirectResponse
    data = await r.form()
    profile_type = data._dict['profile_type']
    id = data._dict['user-selection']
    if profile_type == 'Employee':
        return RedirectResponse(f"/employee/{id}", status_code=303)
    elif profile_type == 'Team':
        return RedirectResponse(f"/team/{id}", status_code=303)

serve()

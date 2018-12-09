# FlaskWebDevelopment

To run the Webapp, go to the root directory where is the *run.py*. Execute the following in the terminal:
```
chmod a+x run.py
./run.py
```
You should see something like this in terminal: *Running on http://127.0.0.1:5000/*

**Click** to the ip address!

# Make os enviroment variable

Python's os.environ probably does not see the environment variable because it is not part of the current environment. Easy to check (no python involved, just shell) using env command or specifically for the case above ```env | grep YOUR_ENVIROMENT_VARIABLE```.

Execute ```export YOUR_ENVIROMENT_VARIABLE="VARIABLE_VALUE"```

Run the python script (or run the minimum python script to expose the variable: ```./flask/bin/python3 -c "import os; print(os.environ.get('YOUR_ENVIROMENT_VARIABLE'))"```. It should be able to see the environment variable.

*Note: Pay attention for quotes because if you use this quote ", then you have to use the other quote ' in your enviroment set-up*

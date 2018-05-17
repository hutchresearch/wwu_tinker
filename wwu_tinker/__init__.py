import json
import requests
import traceback

servers = {production: 'http://ml-tuning.proj.cs.wwu.edu:6060/', 
          development: 'http://ml-tuning.proj.cs.wwu.edu:6061/'}

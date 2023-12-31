from flask import Flask, render_template, request, redirect, url_for, flash,jsonify
import openai
import os
from dotenv import load_dotenv
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
from werkzeug.utils import secure_filename
from datetime import datetime
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')

app = Flask(__name__)
CORS(app)

# Setup logger
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

@app.route('/',methods=['GET'])
def frontend():
    return render_template('index.html')

@app.route('/study_plan_creator_frontend', methods=['POST', 'GET'])
def study_plan_creator_frontend():
    return render_template('study_plan_creator_frontend.html')

@app.route('/explain_concept_frontend', methods=['POST', 'GET'])
def explain_concept_frontend():
    return render_template('explain_concept_frontend.html')

@app.route('/build_project_frontend', methods=['POST', 'GET'])
def build_project_frontend():
    return render_template('build_project_frontend.html')

    

@app.route('/study_plan_creator',methods=['POST','GET'])
def study_plan_creator():
    # print(request.form)
    goal = request.form.get('goal')
    timeframe = request.form.get('timeframe')
    project_type = request.form.get('project_type')
    reference_preference = request.form.get('reference_preference')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'Stated Time on study plan creator: {time}')
    logger.info(f'Goal: {goal}')
    logger.info(f'Timeframe: {timeframe}')
    logger.info(f'Project Type: {project_type}')
    logger.info(f'Reference Preference: {reference_preference}')



    #Define the dictionary
    experts = {
    'coding': 'Senior Engineer',
    'art': 'Artist',
    'art & craft': 'Craftsman',
    'music': 'Musician',
    'dance': 'Dancer',
    'cooking': 'Chef',
    'photography': 'Photographer',
    'writing': 'Author',
    'design': 'Designer',
    'marketing': 'Marketing Specialist',
    'finance': 'Financial Analyst',
    'science': 'Scientist',
    'mathematics': 'Mathematician',
    'history': 'Historian',
    'philosophy': 'Philosopher'
    }

    
    # print(experts)
    # Get the expert for the given project type
    expert = experts.get(project_type, 'General Coding Expert')
    # expert = experts[project_type]
    # print(expert)
    system_prompt =f'''
    Supose you are {expert}. You also works as a tutor of {project_type} and creates study plans to help people to learn different topics.
    You will be provided with the goal of the student, their time commitment, and resource preferences.
    You will create a study plan with timelines and links to resources. 
    Only include relevant resources because time is limited.
    '''

    query = f'''
    {goal}. I can study on this topic for {timeframe}. I only want {reference_preference} as references.
    Make a {timeframe.split()[-1].replace('s', '')}-by-{timeframe.split()[-1].replace('s', '')} plan with detailed steps and references.
    '''

    print(system_prompt, query)

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{
                'role':'system','content':system_prompt,
                'role':'user','content':query

            }],
            max_tokens=2000,
            temperature=0.1
        )
    except Exception as e:
        print(e)
        logger.error(f'Error: {e}')
        return jsonify({"error":e})
    
    #print(response.choices[0].message.content)
    logger.info(f'Response: {response.choices[0].message.content}')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'End Time on study plan creator: {time}')

    return jsonify({"response":response.choices[0].message.content})
    


@app.route('/explain_concept',methods=['POST','GET'])
def explain_concept():
    concept_name = request.form.get('concept_name')
    weekly_time = request.form.get('weekly_time')
    time_frame = request.form.get('time_frame')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'Stated Time on explain concept: {time}')
    logger.info(f'Concept Name: {concept_name}')

    system_prompt ='''
    You will be provided a topic.
    You will provide an explanation on that given topic, assuming that the user has very little relevant knowledge.
    Use analogies and examples in your explanation.
    Also, include examples to implement the concept if applicable.
    '''

    query = f'''Explain "{concept_name}" in details.'''

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[{
                'role':'system','content':system_prompt,
                'role':'user','content':query

            }],
            max_tokens=2000,
            temperature=0.1
        )
    except Exception as e:
        print(e)
        logger.error(f'Error: {e}')
        return jsonify({"error":e})
    
    #print(response.choices[0].message.content)
    logger.info(f'Response: {response.choices[0].message.content}')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'End Time on explain concept: {time}')

    return jsonify({"response":response.choices[0].message.content})






@app.route('/build_project',methods=['POST','GET'])
def build_project():
    goal = request.form.get('goal')
    project_type = request.form.get('project_type')
    time_constraint = request.form.get('time_constraint')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'Stated Time on build project: {time}')
    logger.info(f'Goal: {goal}')
    logger.info(f'Project Type: {project_type}')
    logger.info(f'Time Constraint: {time_constraint}')

    # Define the dictionary
    # experts = {
    # 'coding': 'Senior Programmer',
    # 'art': 'Artist',
    # 'art & craft': 'Craftsman',
    # 'music': 'Musician',
    # 'dance': 'Dancer',
    # 'cooking': 'Chef',
    # 'photography': 'Photographer',
    # 'writing': 'Author',
    # 'design': 'Designer',
    # 'marketing': 'Marketing Specialist',
    # 'finance': 'Financial Analyst',
    # 'science': 'Scientist',
    # 'mathematics': 'Mathematician',
    # 'history': 'Historian',
    # 'philosophy': 'Philosopher'
    # }

    experts = {
    'General Coding': 'Senior Programmer',
    'Data Science': 'Senior Data Scientist',
    'AI Expert': 'AI Expert',
    'Web Developement': 'Senior Web Developer' 
    }


    expert = experts.get(project_type, 'General Coding Expert')

    system_prompt =f'''
    Act as an expert {expert}. User will give the description on a project.
    Provide a project outline.
    Also provide the starter codes for the project.
    '''

    query = f'''
    {goal}. I have {time_constraint} to build this {project_type} project. Provide an outline {time_constraint.split()[-1].replace('s', '')}-by-{time_constraint.split()[-1].replace('s', '')}. 
    Also provide the starter code afterwards.
    '''

    print(system_prompt, query)

    try:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            # model= 'gpt-4',
            messages=[{
                'role':'system','content':system_prompt,
                'role':'user','content':query

            }],
            max_tokens=2000,
            temperature=0.1
        )
    except Exception as e:
        print(e)
        logger.error(f'Error: {e}')
        return jsonify({"error":e})
    
    #print(response.choices[0].message.content)
    logger.info(f'Response: {response.choices[0].message.content}')
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f'End Time on build project : {time}')

    return jsonify({"response":response.choices[0].message.content})



    



if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)

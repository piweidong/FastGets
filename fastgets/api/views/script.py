# coding: utf8
import json
import uuid
import random

from flask import Blueprint, jsonify, request, redirect, abort
from fastgets.core.errors import ApiError
from fastgets.models import ScriptLog
from fastgets.script import Script
from fastgets.job import Job
from fastgets.process import Process


script_blueprint = Blueprint('script', __name__, url_prefix='/script')


@script_blueprint.route('/list')
def script_list_view():
    scripts = Script.get_list()

    job_dict = {
        name: job.to_api_json()
        for name, job in Job.get_dict('script').items()
    }
    process_dict = {
        name: process.to_api_json()
        for name, process in Process.get_dict('script').items()
    }

    scripts = [
        script.to_api_json(
            job=job_dict.get(script.name),
            process=process_dict.get(script.name),
        )
        for script in scripts
    ]

    return jsonify(scripts=scripts)


@script_blueprint.route('/log/list')
def log_list_view():




    scripts = Script.get_list()

    job_dict = {
        name: job.to_api_json()
        for name, job in Job.get_dict('script').items()
    }
    process_dict = {
        name: process.to_api_json()
        for name, process in Process.get_dict('script').items()
    }

    scripts = [
        script.to_api_json(
            job=job_dict.get(script.name),
            process=process_dict.get(script.name),
        )
        for script in scripts
    ]

    return jsonify(scripts=scripts)


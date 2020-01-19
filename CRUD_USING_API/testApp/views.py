from django.shortcuts import render
from testApp.models import Student
from django.views.generic import View
from testApp.utils import is_json
from testApp.mixins import HttpResponseMixin,SerializeMixin
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from testApp.forms import StudentForm

# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class StudentCBV(View, HttpResponseMixin, SerializeMixin):
    def get_object_from_id(self, id):
        try:
            stud = Student.objects.get(id=id)
        except Student.DoesNotExist:
            stud = None
        return stud

    def get(self, request, *args, **kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            json_data = json.dumps({'msg':"Please send Proper valid Data"})
            return self.render_to_http_response(json_data, status= 404)
        pdata = json.loads(data)
        id = pdata.get('id', None)
        if id is not None:
            stud_data = self.get_object_from_id(id)
            if stud_data is None:
                json_data = json.dumps({'msg':"No Macthed Record Found, Please Provide a valid Id"})
                return self.render_to_http_response(json_data, status=404)
            json_data = self.serialize([stud_data],)            
            return self.render_to_http_response(json_data, status=200)
        all_stud_data = Student.objects.all()
        json_data = self.serialize(all_stud_data)
        return self.render_to_http_response(json_data, status=200)

    def delete(self, request, *args, **kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            json_data = json.dumps({'msg':"Please send Proper valid Data"})
            return self.render_to_http_response(json_data, status= 404)
        pdata = json.loads(data)
        id = pdata.get('id', None)
        if id is None:
            json_data = json.dumps({'msg':"Please send a valid Id"})
            return self.render_to_http_response(json_data, status= 404)
        std = self.get_object_from_id(id)
        if std is None:
            json_data = json.dumps({'msg':"No record Found with provided Id, Can not delete Record"})
            return self.render_to_http_response(json_data, status= 404)
        status, deleted_rec = std.delete()
        if status == 1:
            json_data = json.dumps({'msg': "Record deleted Successfully"})
            return self.render_to_http_response(json_data, status=200)

    def post(self, request, *args, **kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            json_data = json.dumps({'msg':"Please send Proper valid Data"})
            return self.render_to_http_response(json_data, status= 404)
        stud_data = json.loads(data)
        form = StudentForm(stud_data)
        if form.is_valid():
            form.save()
            json_data = json.dumps({'msg': "Record Created Successfully"})
            return self.render_to_http_response(json_data, status=200)
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data, status= 404)

    def put(self, request, *args, **kwargs):
        data = request.body
        valid_json = is_json(data)
        if not valid_json:
            json_data = json.dumps({'msg':"Please send Proper valid Data"})
            return self.render_to_http_response(json_data, status= 404)
        #pdata = json.loads(data)
        provided_data = json.loads(data)
        id = provided_data.get('id', None)
        if id is None:
            json_data = json.dumps({'msg':"To perform Updates, Id is Mandatory, Please Provide."})
            return self.render_to_http_response(json_data, status=404)
        stud = self.get_object_from_id(id)
        if stud is None:
            json_data = json.dumps({'msg':"No Matched record Found"})
            return self.render_to_http_response(json_data, status=404)
        original_data = {
            'name' : stud.name,
            'rollno' : stud.rollno,
            'marks' : stud.marks,
            'gf' : stud.gf,
            'bf' : stud.bf
        }
        original_data.update(provided_data)
        form = StudentForm(original_data, instance=stud)
        if form.is_valid():
            form.save()
            json_data = json.dumps({'msg': "Record Updated Successfully"})
            return self.render_to_http_response(json_data, status=200)
        if form.errors:
            json_data = json.dumps(form.errors)
            return self.render_to_http_response(json_data, status= 404)


    

        
        

            


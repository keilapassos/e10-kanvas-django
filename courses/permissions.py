from rest_framework.permissions import BasePermission
        
class CoursePermission(BasePermission):
  def has_permission(self, request, view) :
        
    if request.method == 'POST':
      if request.user.is_authenticated and request.user.is_admin ==  True :
        return True
        
    if request.method == 'GET' :
      return True 

class CoursesByIdPermission(BasePermission) :
  
  def has_permission(self, request, view) :
    if request.method == 'PUT' or request.method == 'PATCH' or request.method == 'DELETE': 
      if request.user.is_authenticated and request.user.is_admin ==  True:
        return True
        
    if request.method == 'GET' :
      return True 
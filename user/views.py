# from django.db import IntegrityError
# from django.shortcuts import get_object_or_404
# from rest_framework.views import APIView, Response

# from rest_framework import status
# from rest_framework.permissions import AllowAny
# from rest_framework_simplejwt.tokens import RefreshToken

# # Create your views here.


# class UserSignupView(APIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]

#     def post(self, request):
#         try:
#             serializer = UserSignupSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 user = serializer.save(request)
#                 RefreshToken.for_user(user)
#                 return Response(
#                     {"msg": "회원가입에 성공하셨습니다"}, status=status.HTTP_202_ACCEPTED
#                 )
#         except IntegrityError:
#             return Response(
#                 {"msg": "회원가입에 실패하셨습니다"}, status=status.HTTP_400_BAD_REQUEST
#             )
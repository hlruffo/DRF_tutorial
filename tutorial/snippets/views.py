from snippets.models import Snippet
from snippets.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class SnippetList(APIView):
    """SnippetList

    Args:
        APIView (view): Apiview
        
    Def:
        Lista todos os snippets ou cria um novo.
        
    """
    def get(self, request, format=None):
        snippet = Snippet.objects.all()
        serializer = SnippetSerializer(snippet, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SnippetDetail(APIView):
    """SnippetDetail

    Args:
        APIView (decorator): Apiview
        
    Def:
        Recupera, atualiza ou deleta um snippet identificado pela pk    
    """
    def get_object(self, pk):
        """get_object

        Args:
            pk (integer): primarykey

        Raises:
            Http404: Se o objeto com a Id não existir -> http 404 -> Not found.
            
        Def:
            Função consulta se o objeto existe com a pk informada.    
        """
        try:
            snippet = Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404
        
    def get(self,request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)
        
    def put(self, request, pk, format=None):
        snippet= self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data)
        
    def delete(self,request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from eco_vision_api_auth_app.models import User


class LeaderboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            offset = int(request.query_params.get('offset', 0))
            limit = int(request.query_params.get('limit', 10))
            limit = min(limit, 100)

            users_ordered = User.objects.filter(
                is_staff=False,
                is_superuser=False
            ).order_by('-exp', '-level', 'id')

            total_users = users_ordered.count()
            leaderboard_users = users_ordered[offset:offset + limit]

            current_user = request.user

            all_user_ids = list(users_ordered.values_list('id', flat=True))
            user_rank = all_user_ids.index(current_user.id) + 1 if current_user.id in all_user_ids else None

            serialized_users = []
            for i, user in enumerate(leaderboard_users, start=offset + 1):
                serialized_users.append({
                    'rank': i,
                    'username': user.username,
                    'email': user.email,
                    'exp': user.exp,
                    'level': user.level,
                    'is_you': user.id == current_user.id
                })

            return Response({
                'leaderboard': serialized_users,
                'your_rank': user_rank,
                'total_users': total_users,
                'offset': offset,
                'limit': limit,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

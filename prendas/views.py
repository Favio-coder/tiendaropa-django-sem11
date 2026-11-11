from django.db.models import Avg, Count, Max, Sum
from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Prenda


def home(request):
    """Vista de inicio basada en función."""
    total_prendas = Prenda.objects.count()
    prendas_disponibles = Prenda.objects.disponibles().count()
    prendas_stock_bajo = Prenda.objects.stock_bajo().count()
    # Ejemplo de annotate/aggregate en la vista de inicio
    precio_promedio = Prenda.objects.aggregate(promedio=Avg('precio'))['promedio']
    stock_total = Prenda.objects.aggregate(total=Sum('stock'))['total']
    categorias_con_conteo = Prenda.objects.values('categoria').annotate(
        total=Count('id')
    ).order_by('categoria')
    context = {
        'total_prendas': total_prendas,
        'prendas_disponibles': prendas_disponibles,
        'prendas_stock_bajo': prendas_stock_bajo,
        'precio_promedio': precio_promedio,
        'stock_total': stock_total,
        'categorias_con_conteo': categorias_con_conteo,
    }
    return render(request, 'prendas/home.html', context)


class PrendaListView(ListView):
    """Vista de catálogo de prendas con filtros por categoría y búsqueda."""

    model = Prenda
    template_name = 'prendas/catalogo.html'
    context_object_name = 'prendas'
    paginate_by = 6

    def get_queryset(self):
        queryset = Prenda.objects.disponibles()
        categoria = self.request.GET.get('categoria')
        query = self.request.GET.get('q')
        if categoria:
            queryset = queryset.por_categoria(categoria)
        if query:
            queryset = queryset.buscar(query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria_actual'] = self.request.GET.get('categoria', '')
        context['query_actual'] = self.request.GET.get('q', '')
        context['categorias'] = Prenda.CATEGORIAS
        return context


class PrendaDetailView(DetailView):
    """Vista de detalle de una prenda."""

    model = Prenda
    template_name = 'prendas/detalle.html'
    context_object_name = 'prenda'

    def get_object(self, queryset=None):
        """Obtiene la prenda por pk con manejo de 404."""
        return super().get_object(queryset)

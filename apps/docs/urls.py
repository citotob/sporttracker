
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from rest_framework.routers import DefaultRouter

# getByVendor = views.VendorPerformanceAPI.as_view({
#     'get': 'upload',
# })
# getAll = views.VendorPerformanceAPI.as_view({
#     'get': 'getAll',
# })
upload = views.DocsAPI.as_view({
    'post': 'upload'
})
upload_doc = views.DocsAPI.as_view({
    'post': 'upload_doc'
})
upgradeversion = views.DocsAPI.as_view({
    'post': 'upgradeversion'
})
upgradeversion_doc = views.DocsAPI.as_view({
    'post': 'upgradeversion_doc'
})
deactivate = views.DocsAPI.as_view({
    'post': 'deactivate'
})
addlike = views.DocsAPI.as_view({
    'post': 'addlike'
})
addview = views.DocsAPI.as_view({
    'post': 'addview'
})
addopen = views.DocsAPI.as_view({
    'post': 'addopen'
})

editText = views.DocsAPI.as_view({
    'put': 'editText'
})

getDocument = views.DocGet.as_view({
    'get': 'getDocument'
})
getDetailDocument = views.DocGet.as_view({
    'get': 'getSubDocument'
})
searchDocument = views.DocGet.as_view({
    'get': 'searchDoc'
})
searchDocuments = views.DocGet.as_view({
    'get': 'searchDocs'
})
searchDocumentpagination = views.DocGet.as_view({
    'get': 'searchDocPaginate'
})
getMost = views.DocGet.as_view({
    'get': 'getDocumentMost'
})
getMostUser = views.DocGet.as_view({
    'get': 'getDocumentMostUser'
})
getDetailByid = views.DocGet.as_view({
    'get': 'getDocumentById'
})
getDetailsByid = views.DocGet.as_view({
    'get': 'getDocumentsById'
})
superadminDashboard = views.Dashboard.as_view({
    'get': 'dashboardSuperAdmin'
})
userDashboard = views.Dashboard.as_view({
    'get': 'dashboardUser'
})

initKategori = views.Category.as_view({
    'post': 'init'
})

getAllKategori = views.Category.as_view({
    'get': 'getAll'
})

getDocumentText = views.DocGet.as_view({
    'get': 'getDocumentText'
})

urlpatterns = [
    path('kategori/init/', initKategori),
    path('kategori/get/', getAllKategori),

    path('dashboard/superadmin/', superadminDashboard),
    path('dashboard/user/', userDashboard),
    path('upload/', upload),
    path('upload_doc/', upload_doc),
    path('upgradeversion/', upgradeversion),
    path('upgradeversion_doc/', upgradeversion_doc),
    path('deactivate/', deactivate),
    path('addlike/', addlike),
    path('addview/', addview),
    path('addopen/', addopen),
    path('editText/', editText),

    path('get/', getDocument),
    path('detail/', getDetailByid),
    path('details/', getDetailsByid),
    path('searchm/', searchDocument),
    path('search/', searchDocuments),
    path('searchpaginate/', searchDocumentpagination),
    path('get/bab/', getDetailDocument),
    path('get/most/', getMost),
    path('get/mostUser/', getMostUser),
    path('getText/', getDocumentText),
]

urlpatterns = format_suffix_patterns(urlpatterns)

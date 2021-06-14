import os
import re
import requests
from django.shortcuts import render
import pyarrow as pa
import pyarrow.dataset as ds
from datetime import datetime
from django.http import JsonResponse
from dataplot.serializers import AssetColumnSerializer
from django.contrib import messages
from dataplot.forms import QueryForm
from django.conf import settings


def get_from_parquet(request):
    if request.GET:
        try:
            query_form = QueryForm(data=request.GET)
            if query_form.is_valid():
                start_date_str = query_form.cleaned_data['start_date']
                end_date_str = query_form.cleaned_data['end_date']
                asset_value = query_form.cleaned_data['asset']
                column_value = query_form.cleaned_data['column']
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
                dataset = ds.dataset(os.path.join(settings.BASE_DIR, 'dataplot/output.parquet'), format='parquet',
                                     partitioning='hive')
                dataset_filtered = dataset.to_table(
                    filter=(ds.field('Asset') == f'{asset_value}') &
                           (ds.field('timestamp') >= pa.array([start_date], pa.timestamp("ns"))[0]) &
                           (ds.field('timestamp') <= pa.array([end_date], pa.timestamp("ns"))[0]),
                    columns=['timestamp', f'{column_value}']
                ).to_pandas()
                table_for_plotting_sorted_by_timestamp = dataset_filtered.sort_values(by=['timestamp'])
                asset_column_test_data = table_for_plotting_sorted_by_timestamp.to_dict('records')
                asset_column_serializer = AssetColumnSerializer(asset_column_test_data, many=True)
                if len(asset_column_serializer.instance) == 0:
                    messages.error(request, 'Error! Query(s) incorrectly entered. Please revise and try again.')
                    return render(request, 'GET_from_parquet.html')
                return JsonResponse(asset_column_serializer.instance, safe=False)
            else:
                return render(request, 'GET_from_parquet.html', {'form': query_form})
        except ValueError:
            messages.error(request, 'Error! Query(s) incorrectly entered. Please revise and try again.')
            return render(request, 'GET_from_parquet.html')
        except TypeError:
            messages.error(request, 'Error! Query(s) incorrectly entered. Please revise and try again.')
            return render(request, 'GET_from_parquet.html')

    return render(request, 'GET_from_parquet.html')


def consume_rest_api(request):
    if request.GET:
        try:
            query_form = QueryForm(data=request.GET)
            if query_form.is_valid():
                start_date = query_form.cleaned_data['start_date']
                end_date = query_form.cleaned_data['end_date']
                asset = query_form.cleaned_data['asset']
                column = query_form.cleaned_data['column']
                consumed_api_result = (requests.get(
                    url=f'https://parquetrestapi.herokuapp.com/?start_date={start_date}&end_date={end_date}'
                        f'&asset={asset}&column={column}').json())
                context = {'consumed_api_result': consumed_api_result}
                return render(request, 'consumed_api_result.html', context)
            else:
                return render(request, 'consume_api.html', {'form': query_form})
        except ValueError:
            messages.error(request, 'Error! Query(s) incorrectly entered. Please revise and try again.')
            return render(request, 'consume_api.html')
        except TypeError:
            messages.error(request, 'Error! Query(s) incorrectly entered. Please revise and try again.')
            return render(request, 'consume_api.html')

    return render(request, 'consume_api.html')


def all_possible_parquet_queries(request):
    dataset = ds.dataset(os.path.join(settings.BASE_DIR, 'dataplot/output.parquet'), format='parquet',
                         partitioning='hive')
    dataset_top_row = str(dataset.head(0))
    columns_raw = re.findall('\\n.*:', dataset_top_row)

    def replace_in_columns_raw(text):
        text_to_replace_list = {'\n': '',
                                ':': '',
                                'timestamp': '',
                                'Asset': '',
                                'Year': '',
                                'Month': ''}
        for k, v in text_to_replace_list.items():
            text = text.replace(k, v)
        return text

    columns_refined = [replace_in_columns_raw(column_text) for column_text in columns_raw]
    timestamp_asset_columns = dataset.to_table(columns=['timestamp', 'Asset']).to_pandas()
    start_date = timestamp_asset_columns['timestamp'].min()
    end_date = timestamp_asset_columns['timestamp'].max()
    assets = timestamp_asset_columns['Asset'].drop_duplicates()

    context = {'start_date': start_date,
               'end_date': end_date,
               'assets': assets,
               'columns': columns_refined
               }
    return render(request, 'all_possible_parquet_queries.html', context)

import click
from earthsat import Goes16


@click.group()
def cli():
    pass

@cli.command()
@click.option('--start', default=None, type=str, help='Insert)

def goes(product, start=None, end=None, bands=None)

@click.command()
@click.option(
    '--user', '-u', type=str, required=True,
    help='Username')
@click.option(
    '--password', '-p', type=str, required=True,
    help='Password')
@click.option(
    '--url', type=str, default='https://scihub.copernicus.eu/apihub/',
    help="""Define API URL. Default URL is
        'https://scihub.copernicus.eu/apihub/'.
        """)
@click.option(
    '--start', '-s', type=str, default='NOW-1DAY',
    help='Start date of the query in the format YYYYMMDD.')
@click.option(
    '--end', '-e', type=str, default='NOW',
    help='End date of the query in the format YYYYMMDD.')
@click.option(
    '--geometry', '-g', type=click.Path(exists=True),
    help='Search area geometry as GeoJSON file.')
@click.option(
    '--uuid', type=str,
    help='Select a specific product UUID instead of a query. Multiple UUIDs can separated by commas.')
@click.option(
    '--name', type=str,
    help='Select specific product(s) by filename. Supports wildcards.')
@click.option(
    '--sentinel', type=click.Choice(['1', '2', '3']),
    help='Limit search to a Sentinel satellite (constellation)')
@click.option(
    '--instrument', type=click.Choice(['MSI', 'SAR-C SAR', 'SLSTR', 'OLCI', 'SRAL']),
    help='Limit search to a specific instrument on a Sentinel satellite.')
@click.option(
    '--producttype', type=click.Choice(['SLC', 'GRD', 'OCN', 'RAW', 'S2MSI1C', 'S2MSI2Ap']),
    help='Limit search to a Sentinel product type.')
@click.option(
    '-c', '--cloud', type=int,
    help='Maximum cloud cover in percent. (requires --sentinel to be 2 or 3)')
@click.option(
    '-o', '--order-by', type=str,
    help="Comma-separated list of keywords to order the result by. "
         "Prefix keywords with '-' for descending order.")
@click.option(
    '-l', '--limit', type=int,
    help='Maximum number of results to return. Defaults to no limit.')
@click.option(
    '--download', '-d', is_flag=True,
    help='Download all results of the query.')
@click.option(
    '--path', type=click.Path(exists=True), default='.',
    help='Set the path where the files will be saved.')
@click.option(
    '--query', '-q', type=str, default=None,
    help="""Extra search keywords you want to use in the query. Separate
        keywords with comma. Example: 'producttype=GRD,polarisationmode=HH'.
        """)
@click.option(
    '--footprints', is_flag=True,
    help="""Create a geojson file search_footprints.geojson with footprints
    and metadata of the returned products.
    """)
@click.version_option(prog_name="awsgoes")
def cli(product, start, end, bands, path):
    """
    """

    goes = Goes16(product, start, end, bands)
    goes.download(path)

import ipaddress
from netbox import exceptions

class Ipam(object):

    def __init__(self, netbox_con):

        self.netbox_con = netbox_con

    def get_ip_addresses(self):
        """Return all ip addresses"""
        return self.netbox_con.get('/ipam/ip-addresses/')

    def get_ip_by_id(self, ip_id):
        """Get IP by it's ID

        :param ip_id: The ID of the ip address
        :return: ip address information
        """
        param = '/ipam/ip-addresses/{}/'.format(ip_id)
        return self.netbox_con.get(param)

    def create_ip_address(self, address, **kwargs):
        """Create a new ip address

        :param address: IP address
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"address": address}
        resp_ok, resp_data = self.netbox_con.post('/ipam/ip-addresses/', required_fields, **kwargs)

        if resp_ok:
            return True
        else:
            raise exceptions.CreateException(resp_data)

    def delete_ip_address(self, address):
        """Delete IP address

        :param address: IP address to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        ip_address_id = self.__convert_ip_address(address)

        if not self.netbox_con.delete('/ipam/ip-addresses/', ip_address_id):
            err_msg = 'Unable to delete IP address: {}'.format(address)
            raise exceptions.DeleteException(err_msg)

        return True

    def __convert_ip_address(self, ip_address):
        """Convert IP address to id

        :param ip_address: The IP address
        :return: ip address id if found otherwise bool False
        """
        for item in self.get_ip_addresses()['results']:
            if item['address'] == ip_address:
                return item['id']
        return False

    def get_ip_prefixes(self):
        """Return all ip prefixes"""
        return self.netbox_con.get('/ipam/prefixes/')

    def create_ip_prefix(self, prefix, **kwargs):
        """Create a new ip prefix

        :param prefix: A valid ip prefix format. The syntax will be checked with the ipaddress module
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"prefix": prefix}

        if ipaddress.ip_network(prefix, strict=True):
            resp_ok, resp_data = self.netbox_con.post('/ipam/prefixes/', required_fields, **kwargs)
            if resp_ok:
                return True
            raise exceptions.CreateException(resp_data)

    def delete_ip_prefix(self, prefix):
        """Delete IP prefix

        :param prefix: IP prefix to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        ip_prefix_id = self.__convert_ip_prefix(prefix)

        if not self.netbox_con.delete('/ipam/prefixes/', ip_prefix_id):
            err_msg = 'Unable to delete IP prefix: {}'.format(prefix)
            raise exceptions.DeleteException(err_msg)

        return True

    def __convert_ip_prefix(self, ip_prefix):
        """Convert IP address to id

        :param ip_prefix: The IP prefix
        :return: ip prefix id if found otherwise bool False
        """
        for item in self.get_ip_addresses()['results']:
            if item['prefix'] == ip_prefix:
                return item['id']
        return False

    def get_vrfs(self):
        """Get all vrfs"""
        return self.netbox_con.get('/ipam/vrfs/')

    def create_vrf(self, name, rd, **kwargs):
        """Create a new vrf

        :param name: Name of the vrf
        :param rd: Route distinguisher in any format
        :param kwargs: Optional arguments
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "rd": rd}
        resp_ok, resp_data = self.netbox_con.post('/ipam/vrfs/', required_fields, **kwargs)

        if resp_ok:
            return True
        else:
            raise exceptions.CreateException(resp_data)

    def delete_vrf(self, vrf):
        """Delete vrf

        :param vrf: Name of vrf to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        vrf_id = self.__convert_vrf(vrf)

        if not self.netbox_con.delete('/ipam/vrfs/', vrf_id):
            err_msg = 'Unable to delete vrf: {}'.format(vrf)
            raise exceptions.DeleteException(err_msg)

        return True

    def __convert_vrf(self, vrf):
        """Convert IP address to id

        :param vrf: The vrf to convert
        :return: vrf id if found otherwise bool False
        """
        for item in self.get_ip_addresses()['results']:
            if item['name'] == vrf:
                return item['id']
        return False

    def get_aggregates(self):
        """Return all aggregates"""
        return self.netbox_con.get('/ipam/aggregates/')

    def create_aggregate(self, prefix, rir, **kwargs):
        """Creates a new aggregate

        :param prefix: IP Prefix
        :param rir: Name of the RIR
        :param kwargs: Optional Arguments
        :return:
        """
        rir_id = self.__convert_rir(rir)
        required_fields = {"prefix": prefix, "rir": rir_id}

        if ipaddress.ip_network(prefix, strict=True):
            resp_ok, resp_data = self.netbox_con.post('/ipam/aggregates/', required_fields, **kwargs)

            if resp_ok:
                return True
            else:
                raise exceptions.CreateException(resp_data)

    def get_rirs(self):
        """Return all rirs"""
        return self.netbox_con.get('/ipam/rirs/')

    def create_rir(self, name, slug):
        """Create new rir

        :param name: Name of the rir
        :param slug: Name of the slug
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "slug": slug}
        resp_ok, resp_data = self.netbox_con.post('/ipam/rirs/', required_fields)

        if resp_ok:
            return True
        else:
            raise exceptions.CreateException(resp_data)

    def delete_rir(self, rir_name):
        """Delete rir

        :param rir_name: rir name to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        rir_id = self.__convert_rir(rir_name)
        if not self.netbox_con.delete('/ipam/rirs/', rir_id):
            err_msg = 'Unable to delete rir {}'.format(rir_name)
            raise exceptions.DeleteException(err_msg)

        return True

    def __convert_rir(self, rir_name):
        """

        :param rir_name:
        :return:
        """
        for item in self.get_rirs()['results']:
            if item['name'] == rir_name:
                return item['id']
        return False

    def get_prefix_roles(self):
        """Return all roles"""
        return self.netbox_con.get('/ipam/roles/')

    def create_prefix_role(self, name, slug):
        """Create new prefix role

        :param name: Name of the prefix role
        :param slug: Name of the slug
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"name": name, "slug": slug}
        resp_ok, resp_data = self.netbox_con.post('/ipam/roles/', required_fields)

        if resp_ok:
            return True
        else:
            raise exceptions.CreateException(resp_data)

    def delete_prefix_role(self, prefix_role):
        """Delete prefix role

        :param prefix_role: prefix role to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        prefix_role_id = self.__convert_prefix_role(prefix_role)
        if not self.netbox_con.delete('/ipam/role/', prefix_role_id):
            err_msg = 'Unable to delete prefix role {}'.format(prefix_role)
            raise exceptions.DeleteException(err_msg)

        return True

    def __convert_prefix_role(self, prefix_role):
        """Convert prefix role to id

        :param prefix_role: Name of the prefix role to convert
        :return: prefix role id if successful otherwise bool False
        """
        for item in self.get_rirs()['results']:
            if item['name'] == prefix_role:
                return item['id']
        return False

    def get_vlans(self):
        """Return all vlans"""
        return self.netbox_con.get('/ipam/vlans')

    def create_vlan(self, vid, vlan_name):
        """Create new vlan

        :param vid: ID of the new vlan
        :param vlan_name: Name of the vlan
        :return: bool True if successful otherwise raise CreateException
        """
        required_fields = {"vid": vid, "name": vlan_name}
        resp_ok, resp_data = self.netbox_con.post('/ipam/vlans/', required_fields)

        if resp_ok:
            return True
        else:
            raise exceptions.CreateException(resp_data)

    def delete_vlan(self, vid):
        """Delete VLAN based on VLAN ID

        :param vid: vlan id to delete
        :return: bool True if successful otherwise raise DeleteException
        """
        vid_id = self.__convert_vlan(vid)
        if not self.netbox_con.delete('/ipam/vlans/', vid_id):
            err_msg = 'Unable to delete VLAN {}'.format(vid)
            raise exceptions.DeleteException(err_msg)

        return True

    def __convert_vlan(self, vid):
        """Convert vlan id to id

        :param vid: VLAN ID
        :return: vlan id if successful otherwise bool False
        """
        for item in self.get_vlans()['results']:
            if item['vid'] == vid:
                return item['id']
        return False
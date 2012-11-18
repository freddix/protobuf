Summary:	Protocol Buffers - Google's data interchange format
Name:		protobuf
Version:	2.4.1
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://protobuf.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	ed436802019c9e1f40cc750eaf78f318
URL:		http://code.google.com/p/protobuf/
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-pythonprov
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Protocol buffers are a flexible, efficient, automated mechanism
for serializing structured data - similar to XML, but smaller,
faster, and simpler. You define how you want your data to be
structured once, then you can use special generated source code
to easily write and read your structured data to and from
a variety of data streams and using a variety of languages.
You can even update your data structure without breaking deployed
programs that are compiled against the "old" format.

Google uses Protocol Buffers for almost all of its internal RPC
protocols and file formats.

%package libs
Summary:	protobuf libraries
Group:		Libraries

%description libs
protobuf libraries.

%package devel
Summary:	Header files for protobuf libraries
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for protobuf libraries.

%package -n python-protobuf
Summary:	Python protocol buffers module
Group:		Development/Languages/Python
%pyrequires_eq	python-libs
Requires:	%{name} = %{version}-%{release}

%description -n python-protobuf
Python protocol buffers module.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-static
%{__make}

cd python
%{__python} setup.py test

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

cd python
%{__python} setup.py install \
	--root=$RPM_BUILD_ROOT \
	--optimize=2

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /usr/sbin/ldconfig
%postun	libs -p /usr/sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES.txt CONTRIBUTORS.txt README.txt
%attr(755,root,root) %{_bindir}/protoc

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %ghost %{_libdir}/libproto*.so.?
%attr(755,root,root) %{_libdir}/libproto*.so.*.*.*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libproto*.so
%{_libdir}/libproto*.la
%{_includedir}/google
%{_pkgconfigdir}/*.pc

%files -n python-protobuf
%defattr(644,root,root,755)
%{py_sitescriptdir}/google
%{py_sitescriptdir}/protobuf-*.pth


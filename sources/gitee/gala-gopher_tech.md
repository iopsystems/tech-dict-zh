基础设施

## 主机

实体名：host

| metrics_name | table_name | metrics_type | unit | metrics description              |
| ------------ | ---------- | ------------ | ---- | -------------------------------- |
| os_version   |            | key          |      | 操作系统版本信息                 |
| hostname     | system_os  | label        |      | 主机名                           |
| kversion     | system_os  | label        |      | 内核版本信息                     |
| cpu_num      | system_os  | label        |      | CPU核数                          |
| memory_MB    | system_os  | label        |      | 内存总量(MB)                     |
| ip_addr      | system_os  | label        |      | 所有的IP地址                     |
| host_type    | system_os  | label        |      | 主机类型（vm或pm）               |
| clock_ticks  | system_os  | label        | Hz   | 系统tick计数                     |
| os_btime     | system_os  | label        |      | 系统启动时间                     |
| value        | system_os  | gauge        |      | 一个固定值作为metric，无实际意义 |

### CPU

实体名：cpu

| metrics_name   | table_name      | metrics_type | unit | metrics description               |
| -------------- | --------------- | ------------ | ---- | --------------------------------- |
| cpu            | system_cpu      | key          |      | CPU编号                           |
| rcu            | system_cpu      | gauge        |      | RCU锁软中断次数                   |
| timer          | system_cpu      | gauge        |      | 定时器软中断次数                  |
| sched          | system_cpu      | gauge        |      | 调度中断次数                      |
| net_rx         | system_cpu      | gauge        |      | 网卡收包中断次数                  |
| user_msec      | system_cpu      | gauge        | ms   | 用户态cpu占用时间（不包括nice）   |
| nice_msec      | system_cpu      | gauge        | ms   | nice用户态cpu占用时间（低优先级） |
| system_msec    | system_cpu      | gauge        | ms   | 内核态cpu占用时间                 |
| idle_msec      | system_cpu      | gauge        | ms   | 空闲状态占用时间                  |
| iowait_msec    | system_cpu      | gauge        | ms   | 等待I/O完成的时间                 |
| irq_msec       | system_cpu      | gauge        | ms   | 硬中断时间                        |
| softirq_msec   | system_cpu      | gauge        | ms   | 软中断时间                        |
| steal_msec     | system_cpu      | gauge        | ms   | 被盗时间                          |
| backlog_drops  | system_cpu      | gauge        |      | softnet_data队列满而丢弃报文数量  |
| rps_count      | system_cpu      | gauge        |      | CPU收到的RPS次数                  |
| util_per       | system_cpu      | gauge        | %    | CPU利用率                         |
| mhz            | system_cpu      | gauge        | Mhz  | CPU时钟频率                       |
| total_used_per | system_cpu_util | gauge        | %    | CPU总利用率                       |

### 内存

#### 系统内存

实体名：mem

| metrics_name  | metrics_type | unit | metrics description |
| ------------- | ------------ | ---- | ------------------- |
| infos         | key          |      | 内存索引            |
| total_kB      | gauge        | KB   | 系统总内存          |
| free_kB       | gauge        | KB   | 未分配物理内存      |
| available_kB  | gauge        | KB   | 系统可用内存        |
| util          | gauge        | %    | 系统内存使用率      |
| buffers_kB    | gauge        | KB   | 块设备占用cache大小 |
| cache_kB      | gauge        | KB   | 系统可用cache大小   |
| active_kB     | gauge        | KB   | 系统活跃cache大小   |
| inactive_kB   | gauge        | KB   | 非活跃cache大小     |
| swap_total_kB | gauge        | KB   | 可用swap空间        |
| swap_free_kB  | gauge        | KB   | 剩余swap空间        |
| swap_util     | gauge        | %    | 交换区的使用率      |

#### 内核内存

实体名：mem

| metrics_name    | metrics_type | unit | metrics description                                          | 支持  |
| --------------- | ------------ | ---- | ------------------------------------------------------------ | ----- |
| kern_kB         | gauge        | KB   | Linux内核所占内存                                            |       |
| slab_kB         | gauge        | KB   | Linux内核态小内存分配器所分配的内存（总计、可回收、不可回收） |       |
| SReclaimable_kB | gauge        | KB   | 可回收slab大小                                               |       |
| Unreclaim_kB    | gauge        | KB   | 不可回收slab大小                                             |       |
| page_kB         | gauge        | KB   | 页表内存                                                     |       |
| vmalloc_kB      | gauge        | KB   | Linux内核通过Vmalloc分配的内存                               |       |
| stack_kB        | gauge        | KB   | 进程的内核堆栈总和                                           |       |
| allocPage_kB    | gauge        | KB   | Linux内核调用AllocPage申请的内存                             | TO BE |

#### 应用内存

实体名：mem

| metrics_name     | metrics_type | unit | metrics description                                          |
| ---------------- | ------------ | ---- | ------------------------------------------------------------ |
| active_file_kB   | gauge        | KB   | 文件缓存（活动）                                             |
| inactive_file_kB | gauge        | KB   | 文件缓存（非活动）                                           |
| active_anon_kB   | gauge        | KB   | 匿名内存（活动）                                             |
| inactive_anon_kB | gauge        | KB   | 匿名内存（非活动）                                           |
| mlocked          | gauge        | KB   | 系统调用锁定内存                                             |
| big_page_kB      | gauge        | KB   | 系统大页内存大小                                             |
| shmem_kB         | gauge        | KB   | 共享内存（tmpfs）。业务进程退出后，经常会忘记删除tmpfs文件，或者在打开状态直接删掉tmpfs文件，都会操作shmem泄露。 |

#### 目录项

实体名：mem

| metrics_name  | metrics_type | unit | metrics description                                    |
| ------------- | ------------ | ---- | ------------------------------------------------------ |
| infos         | key          |      | 内存索引                                               |
| dentry        | gauge        |      | dentry已占用的数量（注意dentry数量过多会引起系统卡顿） |
| unused_dentry | gauge        |      | dentry未使用的数量                                     |
| age_limit     | gauge        | s    | 当内存紧缺时，延迟多少秒后会回收dentry                 |

#### 

### 磁盘

#### 磁盘统计

实体名：disk

| metrics_name | metrics_type | unit                  | metrics description                     |
| ------------ | ------------ | --------------------- | --------------------------------------- |
| disk_name    | key          |                       | blk所在的物理磁盘名称                   |
| rspeed       | gauge        | read   times/second   | 读速率（IOPS）                          |
| wspeed       | gauge        | write   times/second  | 写速率（IOPS）                          |
| rspeed_kB    | gauge        | read   kbytes/second  | 吞吐量                                  |
| wspeed_kB    | gauge        | write   kbytes/second | 吞吐量                                  |
| r_await      | gauge        | ms                    | 读响应时间                              |
| w_await      | gauge        | ms                    | 写响应时间                              |
| rareq        | gauge        |                       | 饱和度(rareq-sz   和 wareq-sz+响应时间) |
| wareq        | gauge        |                       | 饱和度(rareq-sz   和 wareq-sz+响应时间) |
| aqu          | gauge        |                       | 平均队列深度                            |
| util         | gauge        | %                     | 磁盘使用率                              |

#### 磁盘空间占用统计

实体名：disk

| metrics_name | metrics_type | unit | metrics description                |
| ------------ | ------------ | ---- | ---------------------------------- |
| MountOn      | key          |      | 文件系统的挂载点                   |
| MountStatus  | label        |      | 挂载状态                           |
| Fsname       | label        |      | 文件系统名称                       |
| Fstype       | label        |      | 文件系统类型                       |
| Inodes       | label        |      | 节点容量                           |
| IUsed        | gauge        |      | 已使用节点                         |
| IFree        | gauge        |      | 未使用节点                         |
| IUsePer      | gauge        | %    | 已使用节点占比                     |
| Blocks       | gauge        |      | 分区包含的数据块（1024字节）的数目 |
| Used         | gauge        |      | 已用数据块数目                     |
| Free         | gauge        |      | 可用数据块数目                     |
| UsePer       | gauge        | %    | 普通用户空间使用百分比             |

#### Block统计

实体名：block

| metrics_name          | metrics_type | unit  | metrics description            | Support                                |
| --------------------- | ------------ | ----- | ------------------------------ | -------------------------------------- |
| major                 | key          |       | 块对象编号                     | 支持NVME、SCSI、VirtBlock三种类型Block |
| first_minor           | key          |       | 块对象编号                     |                                        |
| blk_type              | label        |       | 块对象类型（比如disk,   part） |                                        |
| blk_name              | label        |       | 块对象名称                     |                                        |
| disk_name             | label        |       | 所属磁盘名称                   |                                        |
| latency_req_max       | gauge        | ns    | block层I/O操作时延最大值       |                                        |
| latency_req_last      | gauge        | ns    | block层I/O操作时延最近值       |                                        |
| latency_req_sum       | gauge        | ns    | block层I/O操作时延总计值       |                                        |
| latency_req_jitter    | gauge        | ns    | block层I/O操作时延抖动         |                                        |
| count_latency_req     | gauge        |       | block层I/O操作操作次数         |                                        |
| latency_driver_max    | gauge        | ns    | 驱动层时延最大值               |                                        |
| latency_driver_last   | gauge        | ns    | 驱动层时延最近值               |                                        |
| latency_driver_sum    | gauge        | ns    | 驱动层时延最总计值             |                                        |
| latency_driver_jitter | gauge        | ns    | 驱动层时延抖动                 |                                        |
| count_latency_driver  | gauge        |       | 驱动层操作次数                 |                                        |
| latency_device_max    | gauge        | ns    | 设备层时延最大值               |                                        |
| latency_device_last   | gauge        | ns    | 设备层时延最近值               |                                        |
| latency_device_sum    | gauge        | ns    | 设备层时延最总计值             |                                        |
| latency_device_jitter | gauge        | ns    | 设备层时延抖动                 |                                        |
| count_latency_device  | gauge        |       | 设备层操作次数                 |                                        |
| err_code              | gauge        |       | block层I/O操作错误码           |                                        |
| read_bytes            | gauge        | bytes | I/O操作读字节数                |                                        |
| write_bytes           | gauge        | bytes | I/O操作写字节数                |                                        |
| access_pagecache      | gauge        |       | 访问过的页数                   |                                        |
| mark_buffer_dirty     | gauge        |       | 脏buffer个数                   |                                        |
| load_page_cache       | gauge        |       | LRU队列缓存页数                |                                        |
| mark_page_dirty       | gauge        |       | 脏page个数                     |                                        |



### 网络

#### 协议栈统计

实体名：net

| metrics_name      | metrics_type | unit | metrics description |
| ----------------- | ------------ | ---- | ------------------- |
| origin            | key          |      | /proc/dev/snmp      |
| tcp_curr_estab    | gauge        |      | 当前的TCP连接数     |
| tcp_in_segs       | gauge        | segs | TCP接收的分片数     |
| tcp_out_segs      | gauge        | segs | TCP发送的分片数     |
| tcp_retrans_segs  | gauge        | segs | TCP重传的分片数     |
| tcp_in_errs       | gauge        |      | TCP入包错误包数     |
| udp_indata_grams  | gauge        | segs | UDP接收包量         |
| udp_outdata_grams | gauge        | segs | UDP发送包量         |

#### 网卡统计

实体名：nic

| metrics_name       | metrics_type | unit     | metrics description    |
| ------------------ | ------------ | -------- | ---------------------- |
| dev_name           | key          |          | 网卡名称               |
| rx_bytes           | gauge        | bytes    | 网卡接收字节数         |
| rx_packets         | gauge        |          | 网卡接收的总数据包数   |
| rx_errs            | gauge        |          | 网卡接收错误的数据包数 |
| rx_dropped         | gauge        |          | 网卡接收丢弃的数据包数 |
| tx_bytes           | gauge        | bytes    | 网卡发送字节数         |
| tx_packets         | gauge        |          | 网卡发送的总数据包数   |
| tx_errs            | gauge        |          | 网卡发送错误的数据包数 |
| tx_dropped         | gauge        |          | 网卡发送丢弃的数据包数 |
| rxspeed_KB         | gauge        | Kbytes/s | 网卡上行速率           |
| txspeed_KB         | gauge        | Kbytes/s | 网卡下行速率           |
| tc_sent_drop       | gauge        |          | TC发送丢包             |
| tc_sent_overlimits | gauge        |          | TC发送队列溢出         |
| tc_backlog         | gauge        |          | TC backlog队列包数量   |
| tc_ecn_mark        | gauge        |          | TC 拥塞标记            |

## 容器性能

实体名：container

| metrics_name                           | metrics_type | unit    | metrics description                             |
| -------------------------------------- | ------------ | ------- | ----------------------------------------------- |
| container_id                           | key          |         | 容器ID                                          |
| cpu_usage_seconds_total                | gauge        | seconds | 容器一秒时间内的整体CPU负载，包括所有CPU Core   |
| cpu_system_seconds_total               | gauge        | seconds | 容器一秒时间内的系统态CPU负载，包括所有CPU Core |
| cpu_user_seconds_total                 | gauge        | seconds | 容器一秒时间内的用户态CPU负载，包括所有CPU Core |
| cpu_cfs_throttled_seconds_total        | gauge        | seconds | 容器限流                                        |
| memory_mapped_file                     | gauge        | bytes   | 容器映射文件占用大小                            |
| memory_cache                           | gauge        | bytes   | 容器Cache内存占用大小                           |
| memory_rss                             | gauge        | bytes   | 容器物理内存占用大小                            |
| memory_working_set_bytes               | gauge        | bytes   | 容器实际占用内存大小（更具参考意义）            |
| start_time_seconds                     | gauge        | seconds | 容器启动时间                                    |
| oom_events_total                       | gauge        | num     | 容器内OOM次数                                   |
| network_receive_bytes_total            | gauge        | bytes   | 容器内网络接收统计                              |
| network_transmit_bytes_total           | gauge        | bytes   | 容器内网络发送统计                              |
| network_receive_errors_total           | gauge        | num     | 容器内网络异常统计（接收错误）                  |
| network_receive_packets_dropped_total  | gauge        | num     | 容器内网络异常统计（接收丢弃）                  |
| network_transmit_errors_total          | gauge        | num     | 容器内网络异常统计（发送错误）                  |
| network_transmit_packets_dropped_total | gauge        | num     | 容器内网络异常统计（发送丢弃）                  |
| fs_reads_bytes_total                   | gauge        | bytes   | 容器I/O读写字节统计 （读）                      |
| fs_writes_bytes_total                  | gauge        | bytes   | 容器I/O读写字节统计  （写）                     |
| fs_read_seconds_total                  | gauge        | seconds | 容器I/O读写时间                                 |
| fs_write_seconds_total                 | gauge        | seconds | 容器I/O读写时间                                 |
| fs_inodes_free                         | gauge        | num     | 容器内inode资源统计（空闲）                     |
| fs_inodes_total                        | gauge        | num     | 容器内inode资源统计（总计）                     |
| file_descriptors                       | gauge        | num     | 容器内文件句柄数量                              |

## 容器SLI性能

实体名：sli_container

| metrics_name       | metrics_type | unit | metrics description                             |
| ------------------ | ------------ | ---- | ----------------------------------------------- |
| container_id       | key          |      | 容器ID                                          |
| cpu_wait_histo     | histogram    | ms   | Latency of CPU wait                             |
| cpu_sleep_histo    | histogram    | ms   | Latency of CPU sleep                            |
| cpu_iowait_histo   | histogram    | ms   | Latency of CPU iowait                           |
| cpu_block_histo    | histogram    | ms   | Latency of CPU block                            |
| cpu_rundelay_histo | histogram    | ms   | Latency of CPU rundelay                         |
| cpu_longsys_histo  | histogram    | ms   | Latency of CPU long systime                     |
| cpu_wait           | gauge        | ms   | Latency of CPU wait                             |
| cpu_sleep          | gauge        | ms   | Latency of CPU sleep                            |
| cpu_iowait         | gauge        | ms   | Latency of CPU iowait                           |
| cpu_block          | gauge        | ms   | Latency of CPU block                            |
| cpu_rundelay       | gauge        | ms   | Latency of CPU rundelay                         |
| cpu_longsys        | gauge        | ms   | Latency of CPU long systime                     |
| mem_reclaim_histo  | histogram    | ms   | Latency of memory reclaim                       |
| mem_compact_histo  | histogram    | ms   | Latency of memory compact                       |
| mem_swapin_histo   | histogram    | ms   | Latency of memory swapin                        |
| mem_reclaim        | gauge        | ms   | Latency of memory reclaim                       |
| mem_compact        | gauge        | ms   | Latency of memory compact                       |
| mem_swapin         | gauge        | ms   | Latency of memory swapin                        |
| bio_latency_histo  | histogram    | ns   | I/O operation delay at the BIO layer (unit: ns) |
| bio_latency        | gauge        | ns   | I/O operation delay at the BIO layer (unit: ns) |

实体名：sli_node

| metrics_name       | metrics_type | unit | metrics description                             |
| ------------------ | ------------ | ---- | ----------------------------------------------- |
| sli_node_key       | key          |      | 容器宿主机的SLI统计                             |
| cpu_wait_histo     | histogram    | ms   | Latency of CPU wait                             |
| cpu_sleep_histo    | histogram    | ms   | Latency of CPU sleep                            |
| cpu_iowait_histo   | histogram    | ms   | Latency of CPU iowait                           |
| cpu_block_histo    | histogram    | ms   | Latency of CPU block                            |
| cpu_rundelay_histo | histogram    | ms   | Latency of CPU rundelay                         |
| cpu_longsys_histo  | histogram    | ms   | Latency of CPU long systime                     |
| cpu_wait           | gauge        | ms   | Latency of CPU wait                             |
| cpu_sleep          | gauge        | ms   | Latency of CPU sleep                            |
| cpu_iowait         | gauge        | ms   | Latency of CPU iowait                           |
| cpu_block          | gauge        | ms   | Latency of CPU block                            |
| cpu_rundelay       | gauge        | ms   | Latency of CPU rundelay                         |
| cpu_longsys        | gauge        | ms   | Latency of CPU long systime                     |
| mem_reclaim_histo  | histogram    | ms   | Latency of memory reclaim                       |
| mem_compact_histo  | histogram    | ms   | Latency of memory compact                       |
| mem_swapin_histo   | histogram    | ms   | Latency of memory swapin                        |
| mem_reclaim        | gauge        | ms   | Latency of memory reclaim                       |
| mem_compact        | gauge        | ms   | Latency of memory compact                       |
| mem_swapin         | gauge        | ms   | Latency of memory swapin                        |
| bio_latency_histo  | histogram    | ns   | I/O operation delay at the BIO layer (unit: ns) |
| bio_latency        | gauge        | ns   | I/O operation delay at the BIO layer (unit: ns) |





## GPU/NPU

待上线



# 应用

## 应用性能

应用性能是指通过eBPF非侵入方式观测应用的黑盒性能指标（RED），观测后以应用维度统计观测结果。

- 观测指标会携带如下标签（除应用公共标签）：

| label name  | 意义                                                   |
| ----------- | ------------------------------------------------------ |
| tgid        | Process ID of l7 session.                              |
| client_ip   | Client IP address of l7 session.                       |
| server_ip   | Server IP address of l7 session.                       |
| server_port | Server Port of l7 session.                             |
| l4_role     | Role of l4 protocol(TCP Client/Server or UDP)          |
| l7_role     | Role of l7 protocol(Client or Server)                  |
| protocol    | Name of l7 protocol(http/http2/mysql...)               |
| ssl         | Indicates whether an SSL-encrypted l7 session is used. |

- 应用性能支持协议包括：HTTP 1.X，PGSQL，#Redis，#DNS，#HTTP2.0，#Dubbo，#MySQL，#Kafka；
- 同时支持加密流的观测，覆盖：openSSL，JSSE, #GoSSL

- 应用性能表呈现三类观测对象：**POD、容器、进程**；具体呈现方式由应用部署方式决定。比如K8S场景，就会以POD维度呈现应用性能数据。

备注：#标注的协议待上线。

| metrics_name | metrics_type | unit | metrics description                                          |
| ------------ | ------------ | ---- | ------------------------------------------------------------ |
| req_count    | gauge        | num  | 应用客户端请求数量（用于计算请求速率qps）                    |
| resp_count   | gauge        | num  | 应用服务端应答数量（用于计算应答速率qps）                    |
| err_count    | gauge        | num  | 应用服务端错误次数（用于计算错误率：err_count /resp_count）  |
| latency_sum  | gauge        | us   | 应用请求时延总和（用于计算平均请求时延：latency_sum/req_count，平均应答时延：latency_sum/resp_count） |
| srtt         | gauge        | us   | 进程TCP时延（tcp_link实体）                                  |
| iowait_ns    | gauge        | us   | 进程I/O阻塞时延（proc实体）                                  |
| cpu          | gauge        | %    | 进程CPU使用率（proc实体）                                    |

## 流量关系

流量关系是指应用之间的访问关系，是由根据应用性能观测数据计算得出。

| metrics_name                 | metrics_type | unit | metrics description                                          |
| ---------------------------- | ------------ | ---- | ------------------------------------------------------------ |
| 客户端应用名（比如POD NAME） | label        |      |                                                              |
| 服务端应用名（比如POD NAME） | label        |      |                                                              |
| req_count                    | gauge        | num  | 应用客户端请求数量（用于计算请求速率qps）                    |
| resp_count                   | gauge        | num  | 应用服务端应答数量（用于计算应答速率qps）                    |
| err_count                    | gauge        | num  | 应用服务端错误次数（用于计算错误率：err_count /resp_count）  |
| latency_sum                  | gauge        | us   | 应用请求时延总和（用于计算平均请求时延：latency_sum/req_count，平均应答时延：latency_sum/resp_count） |
| srtt                         | gauge        | us   | 进程TCP时延（tcp_link实体）                                  |

## 路径拓扑

## 访问日志

待上线

## 应用详细统计

### 应用部署关系

应用部署关系信息由应用性能指标的标签携带，提供包括：

**Node标签**：System ID（集群内唯一），管理IP。

**进程标签**：进程ID、进程名、cmdline。

**网络标签**：clien/server ip、server port、role 标签。

**容器标签**：容器ID、容器名称、容器镜像。

**POD标签**：POD ID，POD IP，Pod Name，Pod Namespace标签。

### 应用详细指标

#### 应用性能

| metrics_name    | metrics_type | unit  | metrics description                                          |
| --------------- | ------------ | ----- | ------------------------------------------------------------ |
| bytes_sent      | gauge        | bytes | 应用发送字节数                                               |
| bytes_recv      | gauge        | bytes | 应用接收字节数                                               |
| segs_sent       | gauge        | bytes | 应用发送seg数                                                |
| segs_recv       | gauge        | bytes | 应用接收seg数                                                |
| throughput_req  | gauge        | num   | 应用请求吞吐量                                               |
| throughput_resp | gauge        | num   | 应用应答吞吐量                                               |
| req_count       | gauge        | num   | 应用客户端请求数量（用于计算请求速率qps）                    |
| resp_count      | gauge        | num   | 应用服务端应答数量（用于计算应答速率qps）                    |
| latency_avg     | gauge        | us    | 应用平均请求时延                                             |
| latency         | histogram    | us    | 应用请求时延                                                 |
| latency_sum     | gauge        | us    | 应用请求时延总和（用于计算平均请求时延：latency_sum/req_count，平均应答时延：latency_sum/resp_count） |
| err_ratio       | gauge        |       | 应用服务端错误错误率                                         |
| err_count       | gauge        | num   | 应用服务端错误次数（用于计算错误率：err_count /resp_count）  |
| srtt            | gauge        | us    | 进程TCP时延（tcp_link实体）                                  |
| iowait_ns       | gauge        | us    | 进程I/O阻塞时延（proc实体）                                  |
| cpu             | gauge        | %     | 进程CPU使用率（proc实体）                                    |



#### 应用系统时延

| metrics_name | metrics_type | unit | metrics descriptio                                           |
| ------------ | ------------ | ---- | ------------------------------------------------------------ |
| sys_latency  | histogram    | ms   | 应用系统时延：应用接收请求时，系统层产生的时延（网络栈、调度） |
| net_latency  | histogram    | ms   | 应用网络时延：应用响应请求，网络层产生的时延（网络栈、网络传输） |

#### 应用I/O

| metrics_name        | metrics_type | unit  | metrics description                                        | 支持  |
| ------------------- | ------------ | ----- | ---------------------------------------------------------- | ----- |
| io_delay            | gauge        | us    | 应用I/O时延                                                | TO BE |
| iowait_ns           | gauge        | ns    | 应用访问I/O产生的wait时延                                  |       |
| bio_latency         | gauge        | us    | 应用访问I/O产生的bio层时延                                 |       |
| bio_err_count       | gauge        | num   | 应用访问I/O产生的BIO错误次数                               |       |
| rchar_bytes         | gauge        | bytes | 应用读字节数量（用于计算应用I/O读速率）                    |       |
| wchar_bytes         | gauge        | bytes | 应用写字节数量（用于计算应用I/O写速率）                    |       |
| fd_count            | gauge        | num   | 应用持有的文件句柄数量                                     |       |
| greater_4k_io_read  | gauge        | num   | 应用内大I/O（大于4K）读操作次数                            |       |
| greater_4k_io_write | gauge        | num   | 应用内大I/O（大于4K）写操作次数                            |       |
| less_4k_io_read     | gauge        | num   | 应用内小I/O（大于4K）读操作次数                            |       |
| less_4k_io_write    | gauge        | num   | 应用内小I/O（大于4K）写操作次数                            |       |
| ns_ext4_read        | gauge        | us    | 应用的文件系统读时延（ext4文件系统，常用文件系统）         |       |
| ns_overlay_read     | gauge        | us    | 应用的文件系统读时延（overlay文件系统，容器场景常使用）    |       |
| ns_tmpfs_read       | gauge        | us    | 应用的文件系统读时延（tmpfs文件系统，临时文件常使用）      |       |
| ns_ext4_write       | gauge        | us    | 应用的文件系统写时延（ext4文件系统，常用文件系统）         |       |
| ns_overlay_write    | gauge        | us    | 应用的文件系统写时延（overlay文件系统，容器场景常使用）    |       |
| ns_tmpfs_write      | gauge        | us    | 应用的文件系统写时延（tmpfs文件系统，临时文件常使用）      |       |
| ns_ext4_flush       | gauge        | us    | 应用的文件系统flush时延（ext4文件系统，常用文件系统）      |       |
| ns_overlay_flush    | gauge        | us    | 应用的文件系统flush时延（overlay文件系统，容器场景常使用） |       |
| ns_tmpfs_flush      | gauge        | us    | 应用的文件系统flush时延（tmpfs文件系统，临时文件常使用）   |       |

#### 应用CPU

| metrics_name     | metrics_type | unit | metrics description                   |
| ---------------- | ------------ | ---- | ------------------------------------- |
| cpu_util   | gauge        | %    | 应用整体CPU使用率（proc实体）       |
| cpu_user_util   | gauge        | %    | 应用用户态CPU使用率（proc实体）       |
| cpu_system_util | gauge        | %    | 应用系统态CPU使用率（proc实体）       |
| offcpu_ns        | gauge        | ns  | 应用调度等待CPU调度的时延（proc实体） |

#### 应用内存

| metrics_name          | metrics_type | unit  | metrics description           |
| --------------------- | ------------ | ----- | ----------------------------- |
| pm_size               | gauge        | bytes | 应用物理内存                  |
| vm_size               | gauge        | bytes | 应用虚拟内存                  |
| minor_pagefault_count | gauge        | num   | 应用产生的轻微级pagefault次数 |
| major_pagefault_count | gauge        | num   | 应用产生的严重级pagefault次数 |
| swap_data_size        | gauge        | bytes | 应用swap区域大小              |
| referenced_size       | gauge        | bytes | 应用引用的page大小            |

#### 应用JVM

| metrics_name               | metrics_type | unit    | metrics description                 |
| -------------------------- | ------------ | ------- | ----------------------------------- |
| threads_current            | gauge        | num     | 应用内当前JVM线程数量               |
| threads_daemon             | gauge        | num     | 应用内守护JVM线程数量               |
| threads_peak               | gauge        | num     | 应用内峰值JVM线程数量               |
| threads_started_total      | counter      | num     | JVM启动后创建线程总数               |
| threads_deadlocked         | gauge        | num     | 应用内死锁JVM线程数量               |
| mem_bytes_used             | gauge        | bytes   | 应用JVM已用内存占用                 |
| mem_bytes_commit           | gauge        | bytes   | 应用JVM提交内存占用                 |
| mem_bytes_max              | gauge        | bytes   | 应用JVM最大内存占用                 |
| mem_bytes_init             | gauge        | bytes   | 应用JVM初始内存占用                 |
| mem_pool_bytes_used        | gauge        | bytes   | 应用JVM已用内存池占用               |
| mem_pool_bytes_commit      | gauge        | bytes   | 应用JVM提交内存池占用               |
| mem_pool_bytes_max         | gauge        | bytes   | 应用JVM最大内存池占用               |
| mem_pool_coll_used_bytes   | gauge        | bytes   | 上次内存回收后应用JVM已用内存池占用 |
| mem_pool_coll_commit_bytes | gauge        | bytes   | 上次内存回收后应用JVM提交内存池占用 |
| mem_pool_coll_max_bytes    | gauge        | bytes   | 上次内存回收后应用JVM最大内存池占用 |
| buffer_pool_used_bytes     | gauge        | bytes   | 应用JVM已用字节数                   |
| buffer_pool_used_buffers   | gauge        | bytes   | 应用JVM已用buffer数                 |
| buffer_pool_capacity_bytes | gauge        | bytes   | 应用JVM内存buffer容量               |
| gc_coll_secs_count         | gauge        | num     | 应用内发生GC次数                    |
| gc_coll_secs_sum           | gauge        | seconds | 应用内GC花费的总时间                |


### 应用网络

#### TCP指标

| metrics_name        | metrics_type | unit    | metrics description                                          |
| ------------------- | ------------ | ------- | ------------------------------------------------------------ |
| rx_bytes            | gauge        | bytes   | 应用内TCP接收字节数（用于计算接收速率bps）（tcp_link实体）   |
| tx_bytes            | gauge        | bytes   | 应用内TCP发送字节数（用于计算发送速率bps）（tcp_link实体）   |
| segs_in             | gauge        | package | 应用内TCP接收包数量（tcp_link实体）                          |
| segs_out            | gauge        | package | 应用内TCP发送包数量（tcp_link实体）                          |
| retran_packets      | gauge        | package | 应用内所有TCP重传包数量（用于计算重传率：retran_packets/segs_out）（tcp_link实体） |
| active_open         | gauge        | num     | 应用内TCP主动建链次数（endpoint_tcp实体）                    |
| active_open_failed  | gauge        | num     | 应用内TCP主动建链失败次数（endpoint_tcp实体）                |
| passive_open_failed | gauge        | num     | 应用内TCP被动建链失败次数（endpoint_tcp实体）                |
| srtt                | histogram    | us      | 应用内TCP P50/P90/P99传输时延（tcp_link实体）                |
| rto                 | histogram    | us      | 应用内TCP P50/P90/P99重传超时时间（tcp_link实体）            |
| ato                 | histogram    | us      | 应用内TCP P50/P90/P99 延时ACK时间（tcp_link实体）            |
| rcv_rtt             | histogram    | us      | 应用内TCP P50/P90/P99接收端传输时延（tcp_link实体）          |
| client_estab_delay  | histogram    | us      | 应用内TCP P50/P90/P99客户端建链时延（tcp_link实体）          |
| server_estab_delay  | histogram    | us      | 应用内TCP P50/P90/P99服务端建链时延（tcp_link实体）          |
| reordering          | histogram    | num     | 应用内TCP P50/P90/P99重排序包数量（tcp_link实体）            |
| zero_win_tx_ratio   | gauge        | %       | 应用内TCP发送零窗比率（tcp_link实体）                        |
| zero_win_rx_ratio   | gauge        | %       | 应用内TCP接收零窗比率（tcp_link实体）                        |
| snd_cwnd            | histogram    | size    | 应用内TCP P50/P90/P99拥塞窗口大小（tcp_link实体）            |
| snd_wnd             | histogram    | size    | 应用内TCP P50/P90/P99发送窗口大小（tcp_link实体）            |
| rcv_wnd             | histogram    | size    | 应用内TCP P50/P90/P99接收窗口大小（tcp_link实体）            |
| avl_snd_wnd         | histogram    | size    | 应用内TCP P50/P90/P99可用发送窗口大小（tcp_link实体）        |
| zero_rcv_wnd_count  | gauge        | num     | 应用内TCP接收零窗次数（tcp_link实体）                        |
| zero_snd_wnd_count  | gauge        | num     | 应用内TCP发送零窗次数（tcp_link实体）                        |
| rst_sent            | gauge        | package | 应用内发送RST报文次数(endpoint_tcp实体)                      |
| rst_recv            | gauge        | package | 应用内接收RST报文次数(endpoint_tcp实体)                      |
| estab_latency       | histogram    |         | 建立TCP连接的时延(endpoint_tcp实体)                          |
| sacked_out          | gauge        | package | 应用内TCP乱序包数量（tcp_link实体）                          |
| lost_out            | gauge        | package | 应用内TCP拥塞丢包数量（tcp_link实体）                        |
| sk_drops            | counter      | package | 应用内TCP丢包数量（IP协议栈丢包）（tcp_link实体）            |
| filter_drops        | gauge        | package | 应用内TCP丢包数量（TCP过滤丢包，比如被eBPF规则过滤）（tcp_link实体） |
| tmout_count         | gauge        | num     | TCP连接超时个数                                              |
| snd_buf_limit_count | gauge        | num     | 分配wmem时的限制                                             |
| rmem_scheduls       | gauge        | num     | rmem调度次数                                                 |
| backlog_drops       | gauge        | num     | 应用的TCP接收数据队列溢出次数（通常是应用处理数据太慢）（tcp_link实体） |
| tcp_oom             | gauge        | num     | 应用内发生TCP OOM次数（通常是因为TCP缓存数据量过多，应用处理慢引发）（tcp_link实体） |
| send_rsts           | gauge        | num     | 发送RST报文次数(tcp_link实体)                                |
| receive_rsts        | gauge        | num     | 接收RST报文次数(tcp_link实体)                                |
| retrans_ratio       | gauge        |         | 重传率(tcp_link实体)                                         |
| syn_sent            | gauge        | package | 应用内SYN报文发送次数(endpoint_tcp实体)                      |
| syn_drop            | gauge        | package | 应用内SYN报文到丢弃次数(endpoint_tcp实体)                    |
| retran_syn          | gauge        | package | 应用内SYN报文重发次数(endpoint_tcp实体)                      |
| synack_sent         | gauge        | package | 应用内synack发送次数(endpoint_tcp实体)                       |
| retran_synacks      | gauge        | package | 应用内synack重发次数(endpoint_tcp实体)                       |
| req_drops           | gauge        | num     | 应用内TCP服务端建链失败次数（关闭侦听后又收到建链请求）(endpoint_tcp实体) |
| accept_overflow     | gauge        | num     | 应用内TCP服务端建链失败次数（TCP发生半连接队列溢出）(endpoint_tcp实体) |
| syn_overflow        | gauge        | num     | 应用内TCP服务端建链失败次数（TCP发生syn队列溢出）(endpoint_tcp实体) |

#### UDP指标

| metrics_name  | metrics_type | unit  | metrics description  |
| ------------- | ------------ | ----- | -------------------- |
| bind_sends    | gauge        | bytes | 应用内UDP流量统计    |
| bind_rcvs     | gauge        | bytes | 应用内UDP流量统计    |
| udp_rcv_drops | gauge        | bytes | 应用内接收侧丢包统计 |

#### DNS指标

| metrics_name | metrics_type | unit | metrics description |
| ------------ | ------------ | ---- | ------------------- |
| domain       | label        |      | 进程访问的DNS域名   |
| delay_avg    | gauge        | ms   | DNS访问平均时延     |
| max_delay    | gauge        | ms   | DNS访问最大时延     |
| error_ratio  | gauge        | %    | DNS访问错误率       |
| count        | gauge        |      | DNS访问次数         |
| error_count  | gauge        |      | DNS访问错误数       |

# 基础中间件



## Kafka监控

### Topic流监控

实体名：kafka_topic_flow

| metrics_name | metrics_type | unit | metrics description                                  | Support        |
| ------------ | ------------ | ---- | ---------------------------------------------------- | -------------- |
| msg_type     | key          |      | 访问类型，producer或consumer                         | 需要修改实体名 |
| client_ip    | key          |      | 客户端IP                                             |                |
| num          | gauge        |      | 在一次采样周期中producer发布或consumer消费的消息数量 |                |
| topic        | key          |      | 消息的topic                                          |                |
| server_ip    | key          |      | kafka server所在主机的网卡IP                         |                |
| server_port  | key          |      | kafka server所绑定的端口号                           |                |

### Topic性能监控

实体名：kafka_topic_metrics

| metrics_name | metrics_type | unit | metrics description          | Support |
| ------------ | ------------ | ---- | ---------------------------- | ------- |
| topic        | key          |      | 消息的topic                  | TO BE   |
| server_ip    | key          |      | kafka server所在主机的网卡IP | TO BE   |
| server_port  | key          |      | kafka server所绑定的端口号   | TO BE   |
| throughput   | histogram    |      | topic 吞吐量                 | TO BE   |

## Nginx/Haproxy监控

### Nginx 负载分担监控

实体名：nginx_link

| metrics_name | metrics_type | unit | metrics description | Support                    |
| ------------ | ------------ | ---- | ------------------- | -------------------------- |
| client_ip    | key          |      | 客户端IP            | 当前仅支持nginx 1.12.1版本 |
| virtual_ip   | key          |      | 虚拟服务器IP        |                            |
| server_ip    | key          |      | 真实服务端IP        |                            |
| virtual_port | key          |      | 虚拟服务器端口      |                            |
| server_port  | key          |      | 真实服务端端口      |                            |
| is_l7        | label        |      | 1—七层LB / 0—四层LB |                            |
| link_count   | gauge        |      | 连接数              |                            |

### Haproxy负载分担监控

实体名：haproxy_link

| metrics_name | metrics_type | unit | metrics description | Support                        |
| ------------ | ------------ | ---- | ------------------- | ------------------------------ |
| client_ip    | key          |      | 客户端IP            | 当前仅支持haproxy 2.5-dev0版本 |
| virtual_ip   | key          |      | 虚拟服务器IP        |                                |
| server_ip    | key          |      | 真实服务端IP        |                                |
| virtual_port | key          |      | 虚拟服务器端口      |                                |
| server_port  | key          |      | 真实服务端端口      |                                |
| protocol     | label        |      | 协议类型(TCP/HTTP)  |                                |
| link_count   | gauge        |      | 连接数              |                                |

###  负载分担流拓扑构建

通过针对TCP连接、Nginx/haproxy负载分担流监控，可以有效构建出前后端应用之间事件TCP拓扑流，如下图所示：

![](./png/nginx_flow.png)



## Redis/PostgreSQL监控

### Redis性能监控

实体名：sli

| metrics_name | metrics_type | unit | metrics description            | Support          |
| ------------ | ------------ | ---- | ------------------------------ | ---------------- |
| tgid         | key          |      | 进程ID                         | 仅支持非加密场景 |
| ins_id       | key          |      | 实例ID                         |                  |
| app          | key          |      | 应用名                         |                  |
| method       | key          |      | 请求方法                       |                  |
| server_ip    | label        |      | 服务端IP                       |                  |
| server_port  | label        |      | 服务端端口                     |                  |
| client_ip    | label        |      | 客户端IP                       |                  |
| client_port  | label        |      | 客户端端口                     |                  |
| rtt_nsec     | gauge        | ns   | Redis协议请求RTT               |                  |
| max_rtt_nsec | gauge        | ns   | Redis协议采样周期内最大请求RTT |                  |

### PostgreSQL性能监控

实体名：sli

| metrics_name | metrics_type | unit | metrics description              | Support                         |
| ------------ | ------------ | ---- | -------------------------------- | ------------------------------- |
| tgid         | key          |      | 进程ID                           | 支持加密场景，openssl 1.1.1版本 |
| ins_id       | key          |      | 实例ID                           |                                 |
| app          | key          |      | 应用名                           |                                 |
| method       | key          |      | 请求方法                         |                                 |
| server_ip    | label        |      | 服务端IP                         |                                 |
| server_port  | label        |      | 服务端端口                       |                                 |
| client_ip    | label        |      | 客户端IP                         |                                 |
| client_port  | label        |      | 客户端端口                       |                                 |
| rtt_nsec     | gauge        | ns   | Postgre协议请求RTT               |                                 |
| max_rtt_nsec | gauge        | ns   | Postgre协议采样周期内最大请求RTT |                                 |
| tps          | gauge        |      | 数据库吞吐量                     | 仅支持openGauss 2.0             |

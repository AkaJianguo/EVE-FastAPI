import request from '@/utils/request'

// 查询组织列表
export function listEntity(query) {
  return request({
    url: '/eve/entity/list',
    method: 'get',
    params: query
  })
}

// 查询组织列表（排除节点）
export function listEntityExcludeChild(entityId) {
  return request({
    url: '/eve/entity/list/exclude/' + entityId,
    method: 'get'
  })
}

// 查询组织详细
export function getEntity(entityId) {
  return request({
    url: '/eve/entity/' + entityId,
    method: 'get'
  })
}

// 新增组织
export function addEntity(data) {
  return request({
    url: '/eve/entity',
    method: 'post',
    data: data
  })
}

// 修改组织
export function updateEntity(data) {
  return request({
    url: '/eve/entity',
    method: 'put',
    data: data
  })
}

// 删除组织
export function delEntity(entityId) {
  return request({
    url: '/eve/entity/' + entityId,
    method: 'delete'
  })
}

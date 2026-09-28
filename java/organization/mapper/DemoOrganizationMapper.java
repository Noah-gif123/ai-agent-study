package com.ruoyi.organization.mapper;

import java.util.List;
import com.ruoyi.organization.domain.DemoOrganization;

/**
 * 机构管理Mapper接口
 * 
 * @author ruoyi
 * @date 2026-06-23
 */
public interface DemoOrganizationMapper 
{
    /**
     * 查询机构管理
     * 
     * @param orgId 机构管理主键
     * @return 机构管理
     */
    public DemoOrganization selectDemoOrganizationByOrgId(Long orgId);

    /**
     * 查询机构管理列表
     * 
     * @param demoOrganization 机构管理
     * @return 机构管理集合
     */
    public List<DemoOrganization> selectDemoOrganizationList(DemoOrganization demoOrganization);

    /**
     * 新增机构管理
     * 
     * @param demoOrganization 机构管理
     * @return 结果
     */
    public int insertDemoOrganization(DemoOrganization demoOrganization);

    /**
     * 修改机构管理
     * 
     * @param demoOrganization 机构管理
     * @return 结果
     */
    public int updateDemoOrganization(DemoOrganization demoOrganization);

    /**
     * 删除机构管理
     * 
     * @param orgId 机构管理主键
     * @return 结果
     */
    public int deleteDemoOrganizationByOrgId(Long orgId);

    /**
     * 批量删除机构管理
     * 
     * @param orgIds 需要删除的数据主键集合
     * @return 结果
     */
    public int deleteDemoOrganizationByOrgIds(Long[] orgIds);
}

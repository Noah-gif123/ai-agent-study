package com.ruoyi.organization.service.impl;

import java.util.List;
import com.ruoyi.common.utils.DateUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.ruoyi.organization.mapper.DemoOrganizationMapper;
import com.ruoyi.organization.domain.DemoOrganization;
import com.ruoyi.organization.service.IDemoOrganizationService;

/**
 * 机构管理Service业务层处理
 * 
 * @author ruoyi
 * @date 2026-06-23
 */
@Service
public class DemoOrganizationServiceImpl implements IDemoOrganizationService 
{
    @Autowired
    private DemoOrganizationMapper demoOrganizationMapper;

    /**
     * 查询机构管理
     * 
     * @param orgId 机构管理主键
     * @return 机构管理
     */
    @Override
    public DemoOrganization selectDemoOrganizationByOrgId(Long orgId)
    {
        return demoOrganizationMapper.selectDemoOrganizationByOrgId(orgId);
    }

    /**
     * 查询机构管理列表
     * 
     * @param demoOrganization 机构管理
     * @return 机构管理
     */
    @Override
    public List<DemoOrganization> selectDemoOrganizationList(DemoOrganization demoOrganization)
    {
        return demoOrganizationMapper.selectDemoOrganizationList(demoOrganization);
    }

    /**
     * 新增机构管理
     * 
     * @param demoOrganization 机构管理
     * @return 结果
     */
    @Override
    public int insertDemoOrganization(DemoOrganization demoOrganization)
    {
        demoOrganization.setCreateTime(DateUtils.getNowDate());
        return demoOrganizationMapper.insertDemoOrganization(demoOrganization);
    }

    /**
     * 修改机构管理
     * 
     * @param demoOrganization 机构管理
     * @return 结果
     */
    @Override
    public int updateDemoOrganization(DemoOrganization demoOrganization)
    {
        demoOrganization.setUpdateTime(DateUtils.getNowDate());
        return demoOrganizationMapper.updateDemoOrganization(demoOrganization);
    }

    /**
     * 批量删除机构管理
     * 
     * @param orgIds 需要删除的机构管理主键
     * @return 结果
     */
    @Override
    public int deleteDemoOrganizationByOrgIds(Long[] orgIds)
    {
        return demoOrganizationMapper.deleteDemoOrganizationByOrgIds(orgIds);
    }

    /**
     * 删除机构管理信息
     * 
     * @param orgId 机构管理主键
     * @return 结果
     */
    @Override
    public int deleteDemoOrganizationByOrgId(Long orgId)
    {
        return demoOrganizationMapper.deleteDemoOrganizationByOrgId(orgId);
    }
}
